/**
 * Unit tests for JobService save/unsave functionality
 * Tests localStorage persistence, error handling, and state management
 */

import jobService from '../jobService';
import { SAMPLE_JOBS } from '../../data/sampleJobs';
import { Job } from '../../types/job';

// Mock localStorage
const localStorageMock = (() => {
  let store: { [key: string]: string } = {};

  return {
    getItem: jest.fn((key: string) => store[key] || null),
    setItem: jest.fn((key: string, value: string) => {
      store[key] = value;
    }),
    removeItem: jest.fn((key: string) => {
      delete store[key];
    }),
    clear: jest.fn(() => {
      store = {};
    }),
  };
})();

// Replace the global localStorage with our mock
Object.defineProperty(window, 'localStorage', {
  value: localStorageMock,
});

// Mock setTimeout to avoid actual delays in tests
jest.useFakeTimers();

describe('JobService Save/Unsave Functionality', () => {
  beforeEach(() => {
    // Clear localStorage mock before each test
    localStorageMock.clear();
    jest.clearAllMocks();
    
    // Clear all timers
    jest.clearAllTimers();
    
    // Reset the service's internal state by clearing saved job IDs
    // This is a bit of a hack since we're testing a singleton, but necessary for isolated tests
    (jobService as any).savedJobIds.clear();
  });

  afterEach(() => {
    jest.runOnlyPendingTimers();
  });

  afterAll(() => {
    jest.useRealTimers();
  });

  describe('saveJob', () => {
    it('should save a job successfully', async () => {
      // Arrange
      const jobId = SAMPLE_JOBS[0].id;

      // Act
      const savePromise = jobService.saveJob(jobId);
      jest.runAllTimers(); // Fast-forward the setTimeout
      const result = await savePromise;

      // Assert
      expect(result).toBe(true);
      expect(jobService.isJobSaved(jobId)).toBe(true);
      expect(localStorageMock.setItem).toHaveBeenCalledWith(
        'savedJobs',
        JSON.stringify([jobId])
      );
    });

    it('should save multiple jobs and maintain them in localStorage', async () => {
      // Arrange
      const jobId1 = SAMPLE_JOBS[0].id;
      const jobId2 = SAMPLE_JOBS[1].id;

      // Act
      const save1Promise = jobService.saveJob(jobId1);
      jest.runAllTimers();
      await save1Promise;

      const save2Promise = jobService.saveJob(jobId2);
      jest.runAllTimers();
      await save2Promise;

      // Assert
      expect(jobService.isJobSaved(jobId1)).toBe(true);
      expect(jobService.isJobSaved(jobId2)).toBe(true);
      
      // Check that localStorage was called with both job IDs
      const lastCall = localStorageMock.setItem.mock.calls[localStorageMock.setItem.mock.calls.length - 1];
      const savedJobIds = JSON.parse(lastCall[1]);
      expect(savedJobIds).toContain(jobId1);
      expect(savedJobIds).toContain(jobId2);
      expect(savedJobIds).toHaveLength(2);
    });

    it('should not duplicate saved jobs', async () => {
      // Arrange
      const jobId = SAMPLE_JOBS[0].id;

      // Act - Save the same job twice
      const save1Promise = jobService.saveJob(jobId);
      jest.runAllTimers();
      await save1Promise;

      const save2Promise = jobService.saveJob(jobId);
      jest.runAllTimers();
      await save2Promise;

      // Assert
      const lastCall = localStorageMock.setItem.mock.calls[localStorageMock.setItem.mock.calls.length - 1];
      const savedJobIds = JSON.parse(lastCall[1]);
      expect(savedJobIds).toHaveLength(1);
      expect(savedJobIds[0]).toBe(jobId);
    });

    it('should handle localStorage errors gracefully', async () => {
      // Arrange
      const jobId = SAMPLE_JOBS[0].id;
      localStorageMock.setItem.mockImplementationOnce(() => {
        throw new Error('localStorage is full');
      });

      // Spy on console.error to verify error logging
      const consoleSpy = jest.spyOn(console, 'error').mockImplementation();

      // Act
      const savePromise = jobService.saveJob(jobId);
      jest.runAllTimers();
      const result = await savePromise;

      // Assert
      expect(result).toBe(false);
      expect(consoleSpy).toHaveBeenCalledWith('Error saving job:', expect.any(Error));
      
      // Cleanup
      consoleSpy.mockRestore();
    });
  });

  describe('unsaveJob', () => {
    it('should unsave a previously saved job', async () => {
      // Arrange - First save a job
      const jobId = SAMPLE_JOBS[0].id;
      const savePromise = jobService.saveJob(jobId);
      jest.runAllTimers();
      await savePromise;

      // Verify it's saved
      expect(jobService.isJobSaved(jobId)).toBe(true);

      // Act - Unsave the job
      const unsavePromise = jobService.unsaveJob(jobId);
      jest.runAllTimers();
      const result = await unsavePromise;

      // Assert
      expect(result).toBe(true);
      expect(jobService.isJobSaved(jobId)).toBe(false);
      expect(localStorageMock.setItem).toHaveBeenCalledWith(
        'savedJobs',
        JSON.stringify([])
      );
    });

    it('should handle unsaving non-existent jobs gracefully', async () => {
      // Arrange
      const nonExistentJobId = 'non-existent-job';

      // Act
      const unsavePromise = jobService.unsaveJob(nonExistentJobId);
      jest.runAllTimers();
      const result = await unsavePromise;

      // Assert
      expect(result).toBe(true); // Should still return true
      expect(jobService.isJobSaved(nonExistentJobId)).toBe(false);
    });

    it('should maintain other saved jobs when unsaving one', async () => {
      // Arrange - Save multiple jobs
      const jobId1 = SAMPLE_JOBS[0].id;
      const jobId2 = SAMPLE_JOBS[1].id;
      const jobId3 = SAMPLE_JOBS[2].id;

      for (const jobId of [jobId1, jobId2, jobId3]) {
        const savePromise = jobService.saveJob(jobId);
        jest.runAllTimers();
        await savePromise;
      }

      // Act - Unsave middle job
      const unsavePromise = jobService.unsaveJob(jobId2);
      jest.runAllTimers();
      await unsavePromise;

      // Assert
      expect(jobService.isJobSaved(jobId1)).toBe(true);
      expect(jobService.isJobSaved(jobId2)).toBe(false);
      expect(jobService.isJobSaved(jobId3)).toBe(true);

      // Check localStorage contains only remaining jobs
      const lastCall = localStorageMock.setItem.mock.calls[localStorageMock.setItem.mock.calls.length - 1];
      const savedJobIds = JSON.parse(lastCall[1]);
      expect(savedJobIds).toContain(jobId1);
      expect(savedJobIds).toContain(jobId3);
      expect(savedJobIds).not.toContain(jobId2);
      expect(savedJobIds).toHaveLength(2);
    });

    it('should handle localStorage errors gracefully during unsave', async () => {
      // Arrange
      const jobId = SAMPLE_JOBS[0].id;
      
      // First save a job
      const savePromise = jobService.saveJob(jobId);
      jest.runAllTimers();
      await savePromise;

      // Mock localStorage error on setItem
      localStorageMock.setItem.mockImplementationOnce(() => {
        throw new Error('localStorage error');
      });

      // Spy on console.error
      const consoleSpy = jest.spyOn(console, 'error').mockImplementation();

      // Act
      const unsavePromise = jobService.unsaveJob(jobId);
      jest.runAllTimers();
      const result = await unsavePromise;

      // Assert
      expect(result).toBe(false);
      expect(consoleSpy).toHaveBeenCalledWith('Error unsaving job:', expect.any(Error));
      
      // Cleanup
      consoleSpy.mockRestore();
    });
  });

  describe('getSavedJobs', () => {
    it('should return empty array when no jobs are saved', async () => {
      // Act
      const getSavedPromise = jobService.getSavedJobs();
      jest.runAllTimers();
      const savedJobs = await getSavedPromise;

      // Assert
      expect(savedJobs).toEqual([]);
      expect(localStorageMock.getItem).toHaveBeenCalledWith('savedJobs');
    });

    it('should return saved jobs from localStorage', async () => {
      // Arrange - Manually set localStorage to simulate existing saved jobs
      const savedJobIds = [SAMPLE_JOBS[0].id, SAMPLE_JOBS[1].id];
      localStorageMock.getItem.mockReturnValueOnce(JSON.stringify(savedJobIds));

      // Act
      const getSavedPromise = jobService.getSavedJobs();
      jest.runAllTimers();
      const savedJobs = await getSavedPromise;

      // Assert
      expect(savedJobs).toHaveLength(2);
      expect(savedJobs[0].id).toBe(SAMPLE_JOBS[0].id);
      expect(savedJobs[1].id).toBe(SAMPLE_JOBS[1].id);
      expect(localStorageMock.getItem).toHaveBeenCalledWith('savedJobs');
    });

    it('should handle corrupted localStorage data gracefully', async () => {
      // Arrange - Set invalid JSON in localStorage
      localStorageMock.getItem.mockReturnValueOnce('invalid-json');

      // Spy on console.error
      const consoleSpy = jest.spyOn(console, 'error').mockImplementation();

      // Act
      const getSavedPromise = jobService.getSavedJobs();
      jest.runAllTimers();
      const savedJobs = await getSavedPromise;

      // Assert
      expect(savedJobs).toEqual([]);
      expect(consoleSpy).toHaveBeenCalledWith('Error fetching saved jobs:', expect.any(Error));
      
      // Cleanup
      consoleSpy.mockRestore();
    });

    it('should filter out non-existent job IDs from localStorage', async () => {
      // Arrange - Include a non-existent job ID in localStorage
      const existingJobId = SAMPLE_JOBS[0].id;
      const nonExistentJobId = 'non-existent-job-id';
      const savedJobIds = [existingJobId, nonExistentJobId];
      localStorageMock.getItem.mockReturnValueOnce(JSON.stringify(savedJobIds));

      // Act
      const getSavedPromise = jobService.getSavedJobs();
      jest.runAllTimers();
      const savedJobs = await getSavedPromise;

      // Assert
      expect(savedJobs).toHaveLength(1);
      expect(savedJobs[0].id).toBe(existingJobId);
    });

    it('should synchronize internal state with localStorage data', async () => {
      // Arrange - Set up localStorage with saved jobs
      const jobId1 = SAMPLE_JOBS[0].id;
      const jobId2 = SAMPLE_JOBS[1].id;
      const savedJobIds = [jobId1, jobId2];
      localStorageMock.getItem.mockReturnValueOnce(JSON.stringify(savedJobIds));

      // Act
      const getSavedPromise = jobService.getSavedJobs();
      jest.runAllTimers();
      await getSavedPromise;

      // Assert - Check that internal state is synchronized
      expect(jobService.isJobSaved(jobId1)).toBe(true);
      expect(jobService.isJobSaved(jobId2)).toBe(true);
    });
  });

  describe('isJobSaved', () => {
    it('should return false for unsaved jobs', () => {
      // Arrange
      const jobId = SAMPLE_JOBS[0].id;

      // Act & Assert
      expect(jobService.isJobSaved(jobId)).toBe(false);
    });

    it('should return true for saved jobs', async () => {
      // Arrange - Save a job first
      const jobId = SAMPLE_JOBS[0].id;
      const savePromise = jobService.saveJob(jobId);
      jest.runAllTimers();
      await savePromise;

      // Act & Assert
      expect(jobService.isJobSaved(jobId)).toBe(true);
    });

    it('should return false after unsaving a job', async () => {
      // Arrange - Save then unsave a job
      const jobId = SAMPLE_JOBS[0].id;
      
      const savePromise = jobService.saveJob(jobId);
      jest.runAllTimers();
      await savePromise;

      const unsavePromise = jobService.unsaveJob(jobId);
      jest.runAllTimers();
      await unsavePromise;

      // Act & Assert
      expect(jobService.isJobSaved(jobId)).toBe(false);
    });
  });

  describe('Integration: Save/Unsave workflow', () => {
    it('should handle complete save/unsave/getSaved workflow', async () => {
      // Arrange
      const jobId1 = SAMPLE_JOBS[0].id;
      const jobId2 = SAMPLE_JOBS[1].id;

      // Act 1: Save jobs
      const save1Promise = jobService.saveJob(jobId1);
      jest.runAllTimers();
      await save1Promise;

      const save2Promise = jobService.saveJob(jobId2);
      jest.runAllTimers();
      await save2Promise;

      // Verify saved state
      expect(jobService.isJobSaved(jobId1)).toBe(true);
      expect(jobService.isJobSaved(jobId2)).toBe(true);

      // Act 2: Get saved jobs
      const getSavedPromise = jobService.getSavedJobs();
      jest.runAllTimers();
      const savedJobs = await getSavedPromise;

      // Verify getSavedJobs returns correct jobs
      expect(savedJobs).toHaveLength(2);
      expect(savedJobs.map((job: Job) => job.id)).toContain(jobId1);
      expect(savedJobs.map((job: Job) => job.id)).toContain(jobId2);

      // Act 3: Unsave one job
      const unsavePromise = jobService.unsaveJob(jobId1);
      jest.runAllTimers();
      await unsavePromise;

      // Verify updated state
      expect(jobService.isJobSaved(jobId1)).toBe(false);
      expect(jobService.isJobSaved(jobId2)).toBe(true);

      // Act 4: Get saved jobs again
      const getSaved2Promise = jobService.getSavedJobs();
      jest.runAllTimers();
      const savedJobsAfterUnsave = await getSaved2Promise;

      // Verify final state
      expect(savedJobsAfterUnsave).toHaveLength(1);
      expect(savedJobsAfterUnsave[0].id).toBe(jobId2);
    });
  });

  describe('Edge cases and error handling', () => {
    it('should handle empty job ID gracefully', async () => {
      // Arrange
      const emptyJobId = '';

      // Act & Assert - Should not throw
      const savePromise = jobService.saveJob(emptyJobId);
      jest.runAllTimers();
      const saveResult = await savePromise;

      const unsavePromise = jobService.unsaveJob(emptyJobId);
      jest.runAllTimers();
      const unsaveResult = await unsavePromise;

      expect(saveResult).toBe(true);
      expect(unsaveResult).toBe(true);
      expect(jobService.isJobSaved(emptyJobId)).toBe(false); // Empty string should be removed from Set
    });

    it('should handle null/undefined job IDs gracefully', async () => {
      // Act & Assert - Should not throw
      expect(() => jobService.isJobSaved(null as any)).not.toThrow();
      expect(() => jobService.isJobSaved(undefined as any)).not.toThrow();
      
      expect(jobService.isJobSaved(null as any)).toBe(false);
      expect(jobService.isJobSaved(undefined as any)).toBe(false);
    });

    it('should handle very long job IDs', async () => {
      // Arrange
      const longJobId = 'a'.repeat(1000);

      // Act
      const savePromise = jobService.saveJob(longJobId);
      jest.runAllTimers();
      const result = await savePromise;

      // Assert
      expect(result).toBe(true);
      expect(jobService.isJobSaved(longJobId)).toBe(true);
    });

    it('should handle localStorage quota exceeded error', async () => {
      // Arrange
      const jobId = SAMPLE_JOBS[0].id;
      localStorageMock.setItem.mockImplementationOnce(() => {
        const error = new Error('Quota exceeded');
        error.name = 'QuotaExceededError';
        throw error;
      });

      // Spy on console.error
      const consoleSpy = jest.spyOn(console, 'error').mockImplementation();

      // Act
      const savePromise = jobService.saveJob(jobId);
      jest.runAllTimers();
      const result = await savePromise;

      // Assert
      expect(result).toBe(false);
      expect(consoleSpy).toHaveBeenCalledWith('Error saving job:', expect.any(Error));
      
      // Cleanup
      consoleSpy.mockRestore();
    });
  });
});
