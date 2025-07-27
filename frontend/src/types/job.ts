// Job-related TypeScript interfaces and types

export interface Job {
  id: string;
  title: string;
  company: string;
  location: string;
  salary: string;
  description: string;
  requirements: string[];
  posted_date: string;
  apply_url: string;
  source: string;
  remote: boolean;
}

export interface JobMatch {
  job_id: string;
  match_score: number;
  matching_skills: string[];
  missing_skills: string[];
}

export interface JobSearchFilters {
  query?: string;
  location?: string;
  remote?: boolean;
  salary_min?: number;
  salary_max?: number;
  skills?: string[];
}

// Ensure this file is treated as a module
export {};