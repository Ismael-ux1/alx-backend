// Import necessary modules
import kue from 'kue';

// Function to create push notification jobs
export default function createPushNotificationsJobs(jobs, queue) {
  // Check if jobs is an array
  if (!Array.isArray(jobs)) {
    throw new Error('Jobs is not an array');
  }

  // For each job in jobs
  for (const jobData of jobs) {
    // Create a job
    const job = queue.create('push_notification_code_3', jobData)
      .save((err) => {
        if (!err) console.log(`Notification job created: ${job.id}`);
      });

    // When the job is complete
    job.on('complete', () => {
      console.log(`Notification job ${job.id} completed`);
    });

    // When the job fails
    job.on('failed', (errorMessage) => {
      console.log(`Notification job ${job.id} failed: ${errorMessage}`);
    });

    // When the job progresses
    job.on('progress', (progress) => {
      console.log(`Notification job ${job.id} ${progress}% complete`);
    });
  }
}
