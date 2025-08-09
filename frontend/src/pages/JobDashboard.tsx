import React, { useState, useEffect, useMemo, useCallback } from 'react';
import { Job, JobSearchFilters } from '../types/job';
import { calculateJobMatch, getMatchedJobs, calculateMatchScore } from '../utils/jobMatching';
import JobCard from '../components/JobCard';
import JobSearch from '../components/JobSearch';
import jobService from '../services/jobService';
import { useAuth } from '../contexts/AuthContext';

const JobDashboard: React.FC = () => {
  const { user, isAuthenticated, token } = useAuth();
  const [jobs, setJobs] = useState<Job[]>([]);
  const [filteredJobs, setFilteredJobs] = useState<Job[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [filters, setFilters] = useState<JobSearchFilters>({});
  const [savedJobIds, setSavedJobIds] = useState<Set<string>>(new Set());
  const [stats, setStats] = useState({
    totalJobs: 0,
    remoteJobs: 0,
    companiesCount: 0,
    averageSalary: undefined as number | undefined
  });
  // Mock user skills - in production, this would come from user context/auth
  const userSkills = ['Python', 'React', 'TypeScript', 'SQL', 'AWS'];

  // useEffect(() => {
  //   loadJobs();
  //   loadSavedJobs();
  //   loadStats();
  // }, []);

  const loadJobs = async () => {
    // try {
    //   setLoading(true);
    //   setError(null);
    //   const jobsData = await jobService.getJobs();
    //   setJobs(jobsData);
    //   setFilteredJobs(jobsData);
    // } catch (err) {
    //   console.error('Error loading jobs:', err);
    //   setError('Failed to load jobs. Please try again.');
    // } finally {
    //   setLoading(false);
    // }
  };

  const loadSavedJobs = async () => {
    try {
      const savedJobs = await jobService.getSavedJobs();
      const savedIds = new Set(savedJobs.map(job => job.id));
      setSavedJobIds(savedIds);
    } catch (err) {
      console.error('Error loading saved jobs:', err);
    }
  };

  const loadStats = async () => {
    try {
      const statsData = await jobService.getJobStats();
      setStats({
        totalJobs: statsData.totalJobs,
        remoteJobs: statsData.remoteJobs,
        companiesCount: statsData.companiesCount,
        averageSalary: statsData.averageSalary
      });
    } catch (err) {
      console.error('Error loading stats:', err);
    }
  };

  const handleFiltersChange = useCallback(async (newFilters: JobSearchFilters) => {
    setFilters(newFilters);
    
    try {
      setLoading(true);
      const searchResults = await jobService.searchJobs(newFilters);
      setFilteredJobs(searchResults);
    } catch (err) {
      console.error('Error searching jobs:', err);
      setError('Search failed. Please try again.');
    } finally {
      setLoading(false);
    }
  }, []);

  const handleSaveJob = async (jobId: string) => {
    try {
      const isCurrentlySaved = savedJobIds.has(jobId);
      
      if (isCurrentlySaved) {
        await jobService.unsaveJob(jobId);
        setSavedJobIds(prev => {
          const newSet = new Set(prev);
          newSet.delete(jobId);
          return newSet;
        });
      } else {
        await jobService.saveJob(jobId);
        setSavedJobIds(prev => new Set(prev).add(jobId));
      }
    } catch (err) {
      console.error('Error saving/unsaving job:', err);
    }
  };

  const handleApplyJob = (job: Job) => {
    // Open application URL
    window.open(job.apply_url, '_blank');
  };

  // Calculate matched jobs with score
  const jobsWithMatches = useMemo(() => {
    return getMatchedJobs(filteredJobs, userSkills);
  }, [filteredJobs, userSkills]);

  const highMatchJobs = useMemo(() => {
    return jobsWithMatches.filter(job => job.matchData.match_score >= 70);
  }, [jobsWithMatches]);

  const averageMatchScore = useMemo(() => {
    return jobsWithMatches.length > 0
    ? Math.round(jobsWithMatches.reduce((sum, job) => sum + job.matchData.match_score, 0) / jobsWithMatches.length)
    : 0;
  }, [jobsWithMatches]);

  if (error) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="text-red-500 text-6xl mb-4">⚠️</div>
          <h2 className="text-2xl font-bold text-gray-900 mb-2">Something went wrong</h2>
          <p className="text-gray-600 mb-4">{error}</p>
          <button
            onClick={loadJobs}
            className="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700"
          >
            Try Again
          </button>
        </div>
      </div>
    );
  }
  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="flex justify-between items-center">
            <div>
              <h1 className="text-3xl font-bold text-gray-900">Job Dashboard</h1>
              <p className="text-gray-600 mt-1">
                Find your next opportunity with AI-powered job matching
              </p>
            </div>
            <div className="flex items-center gap-4">
              <span className="text-sm text-gray-500">
                Your skills: {userSkills.join(', ')}
              </span>
            </div>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <div className="bg-white rounded-lg shadow-md p-6">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <div className="w-8 h-8 bg-blue-500 rounded-md flex items-center justify-center">
                  <svg className="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 13.255A23.931 23.931 0 0112 15c-3.183 0-6.22-.62-9-1.745M16 6V4a2 2 0 00-2-2h-4a2 2 0 00-2-2v2m8 0H8m8 0v2a2 2 0 01-2 2H10a2 2 0 01-2-2V6" />
                  </svg>
                </div>
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-500">Total Jobs</p>
                <p className="text-2xl font-semibold text-gray-900">{stats.totalJobs}</p>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow-md p-6">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <div className="w-8 h-8 bg-green-500 rounded-md flex items-center justify-center">
                  <svg className="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                </div>
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-500">High Matches</p>
                <p className="text-2xl font-semibold text-gray-900">{highMatchJobs.length}</p>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow-md p-6">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <div className="w-8 h-8 bg-yellow-500 rounded-md flex items-center justify-center">
                  <svg className="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z" />
                  </svg>
                </div>
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-500">Saved Jobs</p>
                <p className="text-2xl font-semibold text-gray-900">{savedJobIds.size}</p>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow-md p-6">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <div className="w-8 h-8 bg-purple-500 rounded-md flex items-center justify-center">
                  <svg className="w-5 h-5 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" />
                  </svg>
                </div>
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-500">Avg Match</p>
                <p className="text-2xl font-semibold text-gray-900">{averageMatchScore}%</p>
              </div>
            </div>
          </div>
        </div>

        {/* Search Component */}
        <JobSearch 
          onFiltersChange={handleFiltersChange}
          initialFilters={filters}
          jobCount={filteredJobs.length}
        />

        {/* Loading State */}
        {loading && (
          <div className="text-center py-12">
            <div className="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
            <p className="mt-2 text-gray-600">Loading jobs...</p>
          </div>
        )}

        {/* Job Results */}
        {!loading && (
          <div>
            {/* Results Header */}
            <div className="flex justify-between items-center mb-6">
              <h2 className="text-xl font-semibold text-gray-900">
                {filteredJobs.length === 0 ? 'No jobs found' : `${filteredJobs.length} jobs found`}
              </h2>
              {jobsWithMatches.length > 0 && (
                <div className="flex items-center gap-4 text-sm text-gray-500">
                  <span>Sorted by match score</span>
                  <select className="border border-gray-300 rounded-md px-3 py-1">
                    <option>Best match first</option>
                    <option>Latest first</option>
                    <option>Salary: High to low</option>
                  </select>
                </div>
              )}
            </div>

            {/* Job Grid */}
            {jobsWithMatches.length === 0 ? (
              <div className="text-center py-12">
                <div className="text-gray-400 text-6xl mb-4">🔍</div>
                <h3 className="text-lg font-medium text-gray-900 mb-2">No jobs match your criteria</h3>
                <p className="text-gray-600 mb-4">
                  Try adjusting your filters or search terms to find more opportunities.
                </p>
                <button
                  onClick={() => handleFiltersChange({})}
                  className="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700"
                >
                  Clear all filters
                </button>
              </div>
            ) : (
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                {jobsWithMatches.map((jobWithMatch) => (
                  <JobCard
                    key={jobWithMatch.id}
                    job={jobWithMatch}
                    userSkills={userSkills}
                    matchData={jobWithMatch.matchData}
                    onSave={handleSaveJob}
                    onApply={handleApplyJob}
                    isSaved={savedJobIds.has(jobWithMatch.id)}
                  />
                ))}
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
};
//   return (
//     <div className="min-h-screen bg-gray-50">
//       {/* Header */}
//       <div className="bg-white shadow-sm border-b border-gray-200">
//         <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
//           <div className="flex justify-between items-center">
//             <div>
//               <h1 className="text-3xl font-bold text-gray-900">Job Dashboard</h1>
//               <p className="text-gray-600 mt-1">
//                 Find your next opportunity with AI-powered job matching
//               </p>
//             </div>
//           </div>
//         </div>
//       </div>

//       <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
//         <p>Testing step by step - no blinking so far!</p>
//       </div>
//     </div>
//   );
// };


export default JobDashboard;