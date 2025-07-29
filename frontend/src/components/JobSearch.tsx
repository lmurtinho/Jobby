import React, { useState, useEffect } from 'react';
import { Job, JobSearchFilters } from '../types/job';

interface JobSearchProps {
  onFiltersChange: (filters: JobSearchFilters) => void;
  initialFilters?: JobSearchFilters;
  jobCount?: number;
}

const JobSearch: React.FC<JobSearchProps> = ({
  onFiltersChange,
  initialFilters = {},
  jobCount = 0
}) => {
  const [filters, setFilters] = useState<JobSearchFilters>(initialFilters);
  const [showAdvanced, setShowAdvanced] = useState(false);

  // Debounce the filters change to avoid too many API calls
  useEffect(() => {
    const timeoutId = setTimeout(() => {
      onFiltersChange(filters);
    }, 300);

    return () => clearTimeout(timeoutId);
  }, [filters, onFiltersChange]);

  const handleInputChange = (field: keyof JobSearchFilters, value: any) => {
    setFilters(prev => ({
      ...prev,
      [field]: value
    }));
  };

  const handleSkillsChange = (skillsString: string) => {
    const skills = skillsString
      .split(',')
      .map(skill => skill.trim())
      .filter(skill => skill.length > 0);
    
    handleInputChange('skills', skills.length > 0 ? skills : undefined);
  };

  const clearFilters = () => {
    setFilters({});
  };

  const hasActiveFilters = Object.values(filters).some(value => 
    value !== undefined && value !== '' && (Array.isArray(value) ? value.length > 0 : true)
  );

  return (
    <div className="bg-white rounded-lg shadow-md border border-gray-200 p-6 mb-6">
      {/* Header */}
      <div className="flex justify-between items-center mb-4">
        <h2 className="text-lg font-semibold text-gray-900">
          Search Jobs
          {jobCount > 0 && (
            <span className="ml-2 text-sm text-gray-500">
              ({jobCount} jobs found)
            </span>
          )}
        </h2>
        {hasActiveFilters && (
          <button
            onClick={clearFilters}
            className="text-sm text-blue-600 hover:text-blue-800 underline"
          >
            Clear all filters
          </button>
        )}
      </div>

      {/* Basic Search */}
      <div className="space-y-4">
        {/* Search Query */}
        <div>
          <label htmlFor="search-query" className="block text-sm font-medium text-gray-700 mb-1">
            Job Title, Company, or Keywords
          </label>
          <div className="relative">
            <input
              id="search-query"
              type="text"
              value={filters.query || ''}
              onChange={(e) => handleInputChange('query', e.target.value)}
              placeholder="e.g., Data Scientist, Python, TechCorp"
              className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            />
            <svg
              className="absolute left-3 top-2.5 h-5 w-5 text-gray-400"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
              />
            </svg>
          </div>
        </div>

        {/* Location and Remote */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label htmlFor="location" className="block text-sm font-medium text-gray-700 mb-1">
              Location
            </label>
            <input
              id="location"
              type="text"
              value={filters.location || ''}
              onChange={(e) => handleInputChange('location', e.target.value)}
              placeholder="e.g., São Paulo, Remote"
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            />
          </div>
          
          <div className="flex items-end">
            <label className="flex items-center space-x-2">
              <input
                type="checkbox"
                checked={filters.remote || false}
                onChange={(e) => handleInputChange('remote', e.target.checked ? true : undefined)}
                className="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
              />
              <span className="text-sm font-medium text-gray-700">Remote jobs only</span>
            </label>
          </div>
        </div>
      </div>

      {/* Advanced Filters Toggle */}
      <div className="mt-4">
        <button
          onClick={() => setShowAdvanced(!showAdvanced)}
          className="text-sm text-blue-600 hover:text-blue-800 flex items-center gap-1"
        >
          <svg
            className={`w-4 h-4 transform transition-transform ${showAdvanced ? 'rotate-180' : ''}`}
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
          </svg>
          {showAdvanced ? 'Hide' : 'Show'} advanced filters
        </button>
      </div>

      {/* Advanced Filters */}
      {showAdvanced && (
        <div className="mt-4 pt-4 border-t border-gray-200 space-y-4">
          {/* Salary Range */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Salary Range (USD/month)
            </label>
            <div className="grid grid-cols-2 gap-4">
              <div>
                <input
                  type="number"
                  value={filters.salary_min || ''}
                  onChange={(e) => handleInputChange('salary_min', e.target.value ? parseInt(e.target.value) : undefined)}
                  placeholder="Min salary"
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                />
              </div>
              <div>
                <input
                  type="number"
                  value={filters.salary_max || ''}
                  onChange={(e) => handleInputChange('salary_max', e.target.value ? parseInt(e.target.value) : undefined)}
                  placeholder="Max salary"
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                />
              </div>
            </div>
          </div>

          {/* Skills */}
          <div>
            <label htmlFor="skills" className="block text-sm font-medium text-gray-700 mb-1">
              Required Skills
            </label>
            <input
              id="skills"
              type="text"
              value={filters.skills?.join(', ') || ''}
              onChange={(e) => handleSkillsChange(e.target.value)}
              placeholder="e.g., Python, React, AWS (comma-separated)"
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            />
            <p className="mt-1 text-xs text-gray-500">
              Separate multiple skills with commas
            </p>
          </div>
        </div>
      )}

      {/* Active Filters Summary */}
      {hasActiveFilters && (
        <div className="mt-4 pt-4 border-t border-gray-200">
          <h3 className="text-sm font-medium text-gray-700 mb-2">Active Filters:</h3>
          <div className="flex flex-wrap gap-2">
            {filters.query && (
              <span className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
                Query: "{filters.query}"
                <button
                  onClick={() => handleInputChange('query', undefined)}
                  className="ml-1 text-blue-600 hover:text-blue-800"
                >
                  ×
                </button>
              </span>
            )}
            {filters.location && (
              <span className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-green-100 text-green-800">
                Location: {filters.location}
                <button
                  onClick={() => handleInputChange('location', undefined)}
                  className="ml-1 text-green-600 hover:text-green-800"
                >
                  ×
                </button>
              </span>
            )}
            {filters.remote && (
              <span className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-purple-100 text-purple-800">
                Remote only
                <button
                  onClick={() => handleInputChange('remote', undefined)}
                  className="ml-1 text-purple-600 hover:text-purple-800"
                >
                  ×
                </button>
              </span>
            )}
            {filters.skills && filters.skills.length > 0 && (
              <span className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-yellow-100 text-yellow-800">
                Skills: {filters.skills.join(', ')}
                <button
                  onClick={() => handleInputChange('skills', undefined)}
                  className="ml-1 text-yellow-600 hover:text-yellow-800"
                >
                  ×
                </button>
              </span>
            )}
            {(filters.salary_min || filters.salary_max) && (
              <span className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-red-100 text-red-800">
                Salary: ${filters.salary_min || 0} - ${filters.salary_max || '∞'}
                <button
                  onClick={() => {
                    handleInputChange('salary_min', undefined);
                    handleInputChange('salary_max', undefined);
                  }}
                  className="ml-1 text-red-600 hover:text-red-800"
                >
                  ×
                </button>
              </span>
            )}
          </div>
        </div>
      )}
    </div>
  );
};

export default JobSearch;
