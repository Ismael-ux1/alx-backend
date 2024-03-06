// Import necessary modules
import kue from 'kue';

// Create a queue
const queue = kue.createQueue();

// Function to send a notification
function sendNotification(phoneNumber, message) {
  console.log(`Sending notification to ${phoneNumber}, with message: ${message}`);
}

// Process jobs
queue.process('push_notification_code', function(job, done){
  sendNotification(job.data.phoneNumber, job.data.message);
  done();
});
