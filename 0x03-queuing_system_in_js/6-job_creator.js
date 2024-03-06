// Import necessary modules
import kue from 'kue';

// Create a queue
const queue = kue.createQueue();

// Create an object containing the job data
const jobData = {
  phoneNumber: '1234567890',
  message: 'This is the code to verify your account',
};

// Create a job
const job = queue.create('push_notification_code', jobData)
  .save((err) => {
    if (!err) console.log(`Notification job created: ${job.id}`);
  });

// When the job is complete
job.on('complete', () => {
  console.log('Notification job completed');
});

// When the job fails
job.on('failed', () => {
  console.log('Notification job failed');
});
