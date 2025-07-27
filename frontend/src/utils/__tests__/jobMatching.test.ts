// Unit tests for job matching and search functionality
import { 
  calculateMatchScore, 
  calculateJobMatch, 
  getMatchedJobs 
} from '../jobMatching';
import { Job } from '../../types/job';
import { SAMPLE_JOBS } from '../../data/sampleJobs';

describe('Job Matching Utils', () => {
  describe('calculateMatchScore', () => {
    it('should return 0 when user has no skills', () => {
      const jobSkills = ['Python', 'JavaScript', 'React'];
      const userSkills: string[] = [];
      
      const score = calculateMatchScore(jobSkills, userSkills);
      
      expect(score).toBe(0);
    });

    it('should return 0 when job has no requirements', () => {
      const jobSkills: string[] = [];
      const userSkills = ['Python', 'JavaScript'];
      
      const score = calculateMatchScore(jobSkills, userSkills);
      
      expect(score).toBe(0);
    });

    it('should return 80 when user has all job skills (exact matches)', () => {
      const jobSkills = ['Python', 'SQL', 'React', 'TypeScript'];
      const userSkills = ['Python', 'SQL', 'React', 'TypeScript'];
      
      const score = calculateMatchScore(jobSkills, userSkills);
      
      expect(score).toBe(80); // Our algorithm gives 80% for exact matches
    });

    it('should return 40 when user has half the job skills', () => {
      const jobSkills = ['Python', 'SQL', 'React', 'TypeScript'];
      const userSkills = ['Python', 'SQL'];
      
      const score = calculateMatchScore(jobSkills, userSkills);
      
      expect(score).toBe(40); // Our algorithm: (2/4) * 80 = 40%
    });

    it('should be case insensitive', () => {
      const jobSkills = ['Python', 'SQL', 'React', 'TypeScript'];
      const userSkills = ['python', 'sql', 'react', 'typescript'];
      
      const score = calculateMatchScore(jobSkills, userSkills);
      
      expect(score).toBe(80); // Our algorithm gives 80% for exact matches
    });
  });

  describe('calculateJobMatch', () => {
    const sampleJob: Job = {
      id: "test-1",
      title: "Senior Data Scientist",
      company: "Test Company",
      location: "Remote",
      salary: "$100,000/year",
      description: "Test description",
      requirements: ["Python", "Machine Learning", "SQL"],
      posted_date: "2024-01-01",
      apply_url: "https://test.com",
      source: "Test",
      remote: true
    };

    it('should create a JobMatch with correct score', () => {
      const userSkills = ['Python', 'SQL'];
      
      const match = calculateJobMatch(sampleJob, userSkills);
      
      expect(match.job_id).toBe(sampleJob.id);
      expect(match.match_score).toBeCloseTo(53, 0); // (2/3) * 80 = 53%
      expect(match.matching_skills).toEqual(['Python', 'SQL']);
      expect(match.missing_skills).toEqual(['Machine Learning']);
    });
  });

  describe('getMatchedJobs', () => {
    const userSkills = ['Python', 'JavaScript', 'React'];

    it('should return jobs sorted by match score descending', () => {
      const matches = getMatchedJobs(SAMPLE_JOBS.slice(0, 5), userSkills);
      
      // Verify sorting by match score
      for (let i = 0; i < matches.length - 1; i++) {
        expect(matches[i].matchData.match_score).toBeGreaterThanOrEqual(matches[i + 1].matchData.match_score);
      }
    });
  });
});

describe('Sample Jobs Data Validation', () => {
  it('should have exactly 50 jobs', () => {
    expect(SAMPLE_JOBS).toHaveLength(50);
  });

  it('should have valid job structure for all jobs', () => {
    SAMPLE_JOBS.forEach((job) => {
      expect(job.id).toBeDefined();
      expect(job.title.trim()).toBeTruthy();
      expect(job.company.trim()).toBeTruthy();
      expect(job.requirements.length).toBeGreaterThan(0);
    });
  });
});
