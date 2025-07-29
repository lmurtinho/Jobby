// Job service layer for API communication
// Handles all job-related API calls and data management

import { Job, JobMatch, JobSearchFilters } from '../types/job';
import { SAMPLE_JOBS } from '../data/sampleJobs';

// API base URL - will be replaced with actual backend API
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api/v1';

class JobService {
  private savedJobIds: Set<string> = new Set();

  /**
   * Get all jobs (currently returns sample data)
   * In production, this will call the backend API
   */
  async getJobs(): Promise<Job[]> {
    try {
      // TODO: Replace with actual API call when backend is ready
      // const response = await fetch(`${API_BASE_URL}/jobs`);
      // if (!response.ok) throw new Error('Failed to fetch jobs');
      // return await response.json();
      
      // For now, return sample data with a small delay to simulate API call
      await new Promise(resolve => setTimeout(resolve, 500));
      return [...SAMPLE_JOBS];
    } catch (error) {
      console.error('Error fetching jobs:', error);
      // Fallback to sample data
      return [...SAMPLE_JOBS];
    }
  }

  /**
   * Get a specific job by ID
   */
  async getJobById(jobId: string): Promise<Job | null> {
    try {
      // TODO: Replace with actual API call
      // const response = await fetch(`${API_BASE_URL}/jobs/${jobId}`);
      // if (!response.ok) throw new Error('Job not found');
      // return await response.json();
      
      await new Promise(resolve => setTimeout(resolve, 200));
      const job = SAMPLE_JOBS.find(j => j.id === jobId);
      return job || null;
    } catch (error) {
      console.error('Error fetching job:', error);
      return null;
    }
  }

  /**
   * Search jobs with filters
   */
  async searchJobs(filters: JobSearchFilters): Promise<Job[]> {
    try {
      // TODO: Replace with actual API call
      // const params = new URLSearchParams();
      // Object.entries(filters).forEach(([key, value]) => {
      //   if (value !== undefined) params.append(key, String(value));
      // });
      // const response = await fetch(`${API_BASE_URL}/jobs/search?${params}`);
      // if (!response.ok) throw new Error('Search failed');
      // return await response.json();

      await new Promise(resolve => setTimeout(resolve, 300));
      
      let jobs = [...SAMPLE_JOBS];

      // Apply filters locally (will be done on backend in production)
      if (filters.query) {
        const query = filters.query.toLowerCase();
        jobs = jobs.filter(job =>
          job.title.toLowerCase().includes(query) ||
          job.company.toLowerCase().includes(query) ||
          job.description.toLowerCase().includes(query) ||
          job.requirements.some(skill => skill.toLowerCase().includes(query))
        );
      }

      if (filters.location) {
        const location = filters.location.toLowerCase();
        jobs = jobs.filter(job =>
          job.location.toLowerCase().includes(location)
        );
      }

      if (filters.remote === true) {
        jobs = jobs.filter(job => job.remote);
      }

      if (filters.skills && filters.skills.length > 0) {
        jobs = jobs.filter(job =>
          filters.skills!.some(skill =>
            job.requirements.some(req =>
              req.toLowerCase().includes(skill.toLowerCase())
            )
          )
        );
      }

      if (filters.salary_min || filters.salary_max) {
        jobs = jobs.filter(job => {
          // Simple salary parsing - extract numbers from salary string
          const salaryMatch = job.salary.match(/\$?(\d+,?\d*)/);
          if (!salaryMatch) return true;
          
          const salary = parseInt(salaryMatch[1].replace(',', ''));
          
          if (filters.salary_min && salary < filters.salary_min) return false;
          if (filters.salary_max && salary > filters.salary_max) return false;
          
          return true;
        });
      }

      return jobs;
    } catch (error) {
      console.error('Error searching jobs:', error);
      return [];
    }
  }

  /**
   * Calculate job matches for a user
   */
  async calculateJobMatches(userSkills: string[], jobIds?: string[]): Promise<JobMatch[]> {
    try {
      // TODO: Replace with actual API call
      // const response = await fetch(`${API_BASE_URL}/jobs/matches`, {
      //   method: 'POST',
      //   headers: { 'Content-Type': 'application/json' },
      //   body: JSON.stringify({ user_skills: userSkills, job_ids: jobIds })
      // });
      // if (!response.ok) throw new Error('Failed to calculate matches');
      // return await response.json();

      await new Promise(resolve => setTimeout(resolve, 400));
      
      // Calculate matches locally using imported algorithm
      const { calculateJobMatch } = await import('../utils/jobMatching');
      const jobs = jobIds 
        ? SAMPLE_JOBS.filter(job => jobIds.includes(job.id))
        : SAMPLE_JOBS;

      return jobs.map(job => calculateJobMatch(job, userSkills));
    } catch (error) {
      console.error('Error calculating job matches:', error);
      return [];
    }
  }

  /**
   * Save a job for later
   */
  async saveJob(jobId: string): Promise<boolean> {
    try {
      // TODO: Replace with actual API call
      // const response = await fetch(`${API_BASE_URL}/jobs/${jobId}/save`, {
      //   method: 'POST',
      //   headers: { 'Content-Type': 'application/json' }
      // });
      // if (!response.ok) throw new Error('Failed to save job');

      await new Promise(resolve => setTimeout(resolve, 200));
      this.savedJobIds.add(jobId);
      
      // Store in localStorage for persistence
      const savedJobs = Array.from(this.savedJobIds);
      localStorage.setItem('savedJobs', JSON.stringify(savedJobs));
      
      return true;
    } catch (error) {
      console.error('Error saving job:', error);
      return false;
    }
  }

  /**
   * Unsave a job
   */
  async unsaveJob(jobId: string): Promise<boolean> {
    try {
      // TODO: Replace with actual API call
      // const response = await fetch(`${API_BASE_URL}/jobs/${jobId}/save`, {
      //   method: 'DELETE'
      // });
      // if (!response.ok) throw new Error('Failed to unsave job');

      await new Promise(resolve => setTimeout(resolve, 200));
      this.savedJobIds.delete(jobId);
      
      // Update localStorage
      const savedJobs = Array.from(this.savedJobIds);
      localStorage.setItem('savedJobs', JSON.stringify(savedJobs));
      
      return true;
    } catch (error) {
      console.error('Error unsaving job:', error);
      return false;
    }
  }

  /**
   * Get saved jobs
   */
  async getSavedJobs(): Promise<Job[]> {
    try {
      // TODO: Replace with actual API call
      // const response = await fetch(`${API_BASE_URL}/jobs/saved`);
      // if (!response.ok) throw new Error('Failed to fetch saved jobs');
      // return await response.json();

      await new Promise(resolve => setTimeout(resolve, 300));
      
      // Load from localStorage
      const savedJobsJson = localStorage.getItem('savedJobs');
      if (savedJobsJson) {
        const savedJobIds = JSON.parse(savedJobsJson);
        this.savedJobIds = new Set(savedJobIds);
      }
      
      const savedJobs = SAMPLE_JOBS.filter(job => this.savedJobIds.has(job.id));
      return savedJobs;
    } catch (error) {
      console.error('Error fetching saved jobs:', error);
      return [];
    }
  }

  /**
   * Check if a job is saved
   */
  isJobSaved(jobId: string): boolean {
    return this.savedJobIds.has(jobId);
  }

  /**
   * Get job statistics
   */
  async getJobStats(): Promise<{
    totalJobs: number;
    remoteJobs: number;
    companiesCount: number;
    averageSalary?: number;
  }> {
    try {
      await new Promise(resolve => setTimeout(resolve, 200));
      
      const jobs = SAMPLE_JOBS;
      const remoteJobs = jobs.filter(job => job.remote);
      const companies = new Set(jobs.map(job => job.company));
      
      // Calculate average salary (simplified)
      const salariesWithNumbers = jobs
        .map(job => {
          const match = job.salary.match(/\$(\d+,?\d*)/);
          return match ? parseInt(match[1].replace(',', '')) : null;
        })
        .filter(salary => salary !== null) as number[];
      
      const averageSalary = salariesWithNumbers.length > 0
        ? Math.round(salariesWithNumbers.reduce((sum, salary) => sum + salary, 0) / salariesWithNumbers.length)
        : undefined;

      return {
        totalJobs: jobs.length,
        remoteJobs: remoteJobs.length,
        companiesCount: companies.size,
        averageSalary
      };
    } catch (error) {
      console.error('Error fetching job stats:', error);
      return {
        totalJobs: 0,
        remoteJobs: 0,
        companiesCount: 0
      };
    }
  }

  /**
   * Filter jobs by query string (alias for searchJobs for backwards compatibility)
   */
  async filterJobs(query: string): Promise<Job[]> {
    return this.searchJobs({ query });
  }

  /**
   * Initialize saved jobs from localStorage
   */
  initializeSavedJobs(): void {
    try {
      const savedJobsJson = localStorage.getItem('savedJobs');
      if (savedJobsJson) {
        const savedJobIds = JSON.parse(savedJobsJson);
        this.savedJobIds = new Set(savedJobIds);
      }
    } catch (error) {
      console.error('Error initializing saved jobs:', error);
    }
  }
}

// Create and export a singleton instance
const jobService = new JobService();
jobService.initializeSavedJobs();

export default jobService;
