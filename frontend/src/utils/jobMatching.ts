// Job matching algorithm utilities
// Simple but extensible matching logic that can be enhanced with ML later

import { Job, JobMatch } from '../types/job';

/**
 * Calculate match score between user skills and job requirements
 * @param jobSkills - Array of required skills for the job
 * @param userSkills - Array of user's skills
 * @returns Match score from 0-100
 */
export const calculateMatchScore = (jobSkills: string[], userSkills: string[]): number => {
  if (!jobSkills || jobSkills.length === 0) return 0;
  if (!userSkills || userSkills.length === 0) return 0;

  // Simple keyword matching - will be replaced with ML later
  const normalizedJobSkills = jobSkills.map(skill => skill.toLowerCase().trim());
  const normalizedUserSkills = userSkills.map(skill => skill.toLowerCase().trim());

  // Count exact matches
  const exactMatches = normalizedJobSkills.filter(jobSkill =>
    normalizedUserSkills.includes(jobSkill)
  );

  // Count partial matches (contains)
  const partialMatches = normalizedJobSkills.filter(jobSkill =>
    normalizedUserSkills.some(userSkill =>
      userSkill.includes(jobSkill) || jobSkill.includes(userSkill)
    )
  );

  // Calculate score: exact matches weighted higher
  const exactScore = (exactMatches.length / normalizedJobSkills.length) * 80;
  const partialScore = ((partialMatches.length - exactMatches.length) / normalizedJobSkills.length) * 20;

  const totalScore = exactScore + partialScore;
  return Math.round(Math.min(100, Math.max(0, totalScore)));
};

/**
 * Calculate detailed job match including matching and missing skills
 * @param job - Job object to match against
 * @param userSkills - User's skills array
 * @returns JobMatch object with detailed breakdown
 */
export const calculateJobMatch = (job: Job, userSkills: string[]): JobMatch => {
  const normalizedJobSkills = job.requirements.map(skill => skill.toLowerCase().trim());
  const normalizedUserSkills = userSkills.map(skill => skill.toLowerCase().trim());

  // Find matching skills
  const matchingSkills = job.requirements.filter(jobSkill =>
    normalizedUserSkills.some(userSkill =>
      userSkill.toLowerCase().includes(jobSkill.toLowerCase()) ||
      jobSkill.toLowerCase().includes(userSkill.toLowerCase())
    )
  );

  // Find missing skills
  const missingSkills = job.requirements.filter(jobSkill =>
    !normalizedUserSkills.some(userSkill =>
      userSkill.toLowerCase().includes(jobSkill.toLowerCase()) ||
      jobSkill.toLowerCase().includes(userSkill.toLowerCase())
    )
  );

  const matchScore = calculateMatchScore(job.requirements, userSkills);

  return {
    job_id: job.id,
    match_score: matchScore,
    matching_skills: matchingSkills,
    missing_skills: missingSkills
  };
};

/**
 * Filter and sort jobs by match score
 * @param jobs - Array of jobs to filter
 * @param userSkills - User's skills
 * @param minScore - Minimum match score threshold (default: 0)
 * @returns Array of jobs with match data, sorted by score
 */
export const getMatchedJobs = (
  jobs: Job[], 
  userSkills: string[], 
  minScore: number = 0
): (Job & { matchData: JobMatch })[] => {
  return jobs
    .map(job => ({
      ...job,
      matchData: calculateJobMatch(job, userSkills)
    }))
    .filter(jobWithMatch => jobWithMatch.matchData.match_score >= minScore)
    .sort((a, b) => b.matchData.match_score - a.matchData.match_score);
};

/**
 * Get skill frequency analysis from job requirements
 * @param jobs - Array of jobs to analyze
 * @returns Object with skill frequencies
 */
export const analyzeSkillFrequency = (jobs: Job[]): Record<string, number> => {
  const skillCounts: Record<string, number> = {};

  jobs.forEach(job => {
    job.requirements.forEach(skill => {
      const normalizedSkill = skill.trim();
      skillCounts[normalizedSkill] = (skillCounts[normalizedSkill] || 0) + 1;
    });
  });

  return skillCounts;
};

/**
 * Get top missing skills across all jobs for a user
 * @param jobs - Array of jobs to analyze
 * @param userSkills - User's current skills
 * @returns Array of missing skills sorted by frequency
 */
export const getTopMissingSkills = (
  jobs: Job[], 
  userSkills: string[]
): { skill: string; frequency: number; percentage: number }[] => {
  const normalizedUserSkills = userSkills.map(skill => skill.toLowerCase().trim());
  const missingSkillCounts: Record<string, number> = {};

  jobs.forEach(job => {
    job.requirements.forEach(skill => {
      const normalizedSkill = skill.toLowerCase().trim();
      const hasSkill = normalizedUserSkills.some(userSkill =>
        userSkill.includes(normalizedSkill) || normalizedSkill.includes(userSkill)
      );

      if (!hasSkill) {
        missingSkillCounts[skill] = (missingSkillCounts[skill] || 0) + 1;
      }
    });
  });

  const totalJobs = jobs.length;
  return Object.entries(missingSkillCounts)
    .map(([skill, frequency]) => ({
      skill,
      frequency,
      percentage: Math.round((frequency / totalJobs) * 100)
    }))
    .sort((a, b) => b.frequency - a.frequency);
};

/**
 * Calculate average match score for a user across all jobs
 * @param jobs - Array of jobs
 * @param userSkills - User's skills
 * @returns Average match score
 */
export const calculateAverageMatchScore = (jobs: Job[], userSkills: string[]): number => {
  if (jobs.length === 0) return 0;

  const totalScore = jobs.reduce((sum, job) => {
    return sum + calculateMatchScore(job.requirements, userSkills);
  }, 0);

  return Math.round(totalScore / jobs.length);
};

/**
 * Simple job filtering by query string
 * @param jobs - Array of jobs to filter
 * @param query - Search query
 * @returns Filtered jobs array
 */
export const filterJobsByQuery = (jobs: Job[], query: string): Job[] => {
  if (!query || query.trim() === '') return jobs;

  const normalizedQuery = query.toLowerCase().trim();
  
  return jobs.filter(job =>
    job.title.toLowerCase().includes(normalizedQuery) ||
    job.company.toLowerCase().includes(normalizedQuery) ||
    job.location.toLowerCase().includes(normalizedQuery) ||
    job.description.toLowerCase().includes(normalizedQuery) ||
    job.requirements.some(skill => skill.toLowerCase().includes(normalizedQuery))
  );
};
