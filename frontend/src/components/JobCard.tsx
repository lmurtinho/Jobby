import React from 'react';
import { Job, JobMatch } from '../types/job';

interface JobCardProps {
  job: Job;
  userSkills: string[];
  matchData?: JobMatch;
  onSave?: (jobId: string) => void;
  onApply?: (job: Job) => void;
  isSaved?: boolean;
}

const JobCard: React.FC<JobCardProps> = ({
  job,
  userSkills,
  matchData,
  onSave,
  onApply,
  isSaved = false
}) => {
  const handleSaveClick = () => {
    if (onSave) {
      onSave(job.id);
    }
  };

  const handleApplyClick = () => {
    if (onApply) {
      onApply(job);
    } else {
      // Default behavior: open apply URL
      window.open(job.apply_url, '_blank');
    }
  };

  const getMatchScoreColor = (score: number): string => {
    if (score >= 80) return 'text-green-600 bg-green-100';
    if (score >= 60) return 'text-yellow-600 bg-yellow-100';
    if (score >= 40) return 'text-orange-600 bg-orange-100';
    return 'text-red-600 bg-red-100';
  };

  const formatSalary = (salary: string): string => {
    return salary.replace(/\$/g, '$').replace(/R\$/g, 'R$');
  };

  const formatDate = (dateString: string): string => {
    try {
      const date = new Date(dateString);
      return date.toLocaleDateString('pt-BR');
    } catch {
      return dateString;
    }
  };

  return (
    <div className="bg-white rounded-lg shadow-md border border-gray-200 p-6 hover:shadow-lg transition-shadow duration-200">
      {/* Header */}
      <div className="flex justify-between items-start mb-4">
        <div className="flex-1">
          <h3 className="text-xl font-semibold text-gray-900 mb-1">
            {job.title}
          </h3>
          <p className="text-lg text-gray-600 mb-2">{job.company}</p>
          <div className="flex items-center gap-4 text-sm text-gray-500">
            <span className="flex items-center gap-1">
              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
              </svg>
              {job.location}
            </span>
            {job.remote && (
              <span className="bg-blue-100 text-blue-800 px-2 py-1 rounded-full text-xs font-medium">
                Remote
              </span>
            )}
            <span>{formatDate(job.posted_date)}</span>
          </div>
        </div>
        
        {/* Match Score */}
        {matchData && (
          <div className={`px-3 py-1 rounded-full text-sm font-medium ${getMatchScoreColor(matchData.match_score)}`}>
            {matchData.match_score}% match
          </div>
        )}
      </div>

      {/* Salary */}
      <div className="mb-4">
        <span className="text-lg font-semibold text-green-600">
          {formatSalary(job.salary)}
        </span>
      </div>

      {/* Description */}
      <p className="text-gray-700 mb-4 line-clamp-3">
        {job.description}
      </p>

      {/* Skills */}
      <div className="mb-4">
        <h4 className="text-sm font-medium text-gray-900 mb-2">Required Skills:</h4>
        <div className="flex flex-wrap gap-2">
          {job.requirements.map((skill, index) => {
            const isUserSkill = userSkills.some(userSkill =>
              userSkill.toLowerCase().includes(skill.toLowerCase()) ||
              skill.toLowerCase().includes(userSkill.toLowerCase())
            );
            
            return (
              <span
                key={index}
                className={`px-2 py-1 rounded-md text-xs font-medium ${
                  isUserSkill
                    ? 'bg-green-100 text-green-800 border border-green-200'
                    : 'bg-gray-100 text-gray-700 border border-gray-200'
                }`}
              >
                {skill}
              </span>
            );
          })}
        </div>
      </div>

      {/* Match Details */}
      {matchData && (
        <div className="mb-4 p-3 bg-gray-50 rounded-md">
          <div className="grid grid-cols-2 gap-4 text-sm">
            <div>
              <span className="font-medium text-gray-700">Matching Skills:</span>
              <span className="ml-2 text-green-600">
                {matchData.matching_skills.length}
              </span>
            </div>
            <div>
              <span className="font-medium text-gray-700">Missing Skills:</span>
              <span className="ml-2 text-red-600">
                {matchData.missing_skills.length}
              </span>
            </div>
          </div>
          
          {matchData.missing_skills.length > 0 && (
            <div className="mt-2">
              <span className="text-xs text-gray-600">
                Missing: {matchData.missing_skills.slice(0, 3).join(', ')}
                {matchData.missing_skills.length > 3 && ` +${matchData.missing_skills.length - 3} more`}
              </span>
            </div>
          )}
        </div>
      )}

      {/* Actions */}
      <div className="flex gap-3">
        <button
          onClick={handleApplyClick}
          className="flex-1 bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700 transition-colors duration-200 font-medium"
        >
          Apply Now
        </button>
        <button
          onClick={handleSaveClick}
          className={`px-4 py-2 rounded-md border transition-colors duration-200 font-medium ${
            isSaved
              ? 'bg-yellow-50 border-yellow-300 text-yellow-700 hover:bg-yellow-100'
              : 'bg-white border-gray-300 text-gray-700 hover:bg-gray-50'
          }`}
        >
          {isSaved ? 'Saved' : 'Save'}
        </button>
      </div>

      {/* Source */}
      <div className="mt-3 text-xs text-gray-400 text-right">
        via {job.source}
      </div>
    </div>
  );
};

export default JobCard;
