// Import necessary modules
import express from 'express';
import redis from 'redis';
import { promisify } from 'util';
import kue from 'kue';

// Create a Redis client
const client = redis.createClient();

// Promisify the get and set methods
const getAsync = promisify(client.get).bind(client);
const setAsync = promisify(client.set).bind(client);

// Function to reserve a seat
async function reserveSeat(number) {
  await setAsync('available_seats', number);
}

// Async function to get current available seats
async function getCurrentAvailableSeats() {
  const seats = await getAsync('available_seats');
  return seats;
}

// Initialize the number of available seats and reservationEnabled
let reservationEnabled = true;
reserveSeat(50);

// Create a Kue queue
const queue = kue.createQueue();

// Create an Express server
const app = express();

// Route to get the number of available seats
app.get('/available_seats', async (req, res) => {
  const seats = await getCurrentAvailableSeats();
  res.json({ numberOfAvailableSeats: seats });
});

// Route to reserve a seat
app.get('/reserve_seat', (req, res) => {
  if (!reservationEnabled) {
    res.json({ status: 'Reservation are blocked' });
  } else {
    const job = queue.create('reserve_seat')
      .save((err) => {
        if (err) {
          res.json({ status: 'Reservation failed' });
        } else {
          console.log(`Seat reservation job ${job.id} created`);
          res.json({ status: 'Reservation in process' });
        }
      });

    job.on('complete', () => {
      console.log(`Seat reservation job ${job.id} completed`);
    });

    job.on('failed', (errorMessage) => {
      console.log(`Seat reservation job ${job.id} failed: ${errorMessage}`);
    });
  }
});

// Route to process the queue
app.get('/process', (req, res) => {
  queue.process('reserve_seat', async (job, done) => {
    let seats = await getCurrentAvailableSeats();
    seats--;

    if (seats < 0) {
      done(new Error('Not enough seats available'));
    } else {
      await reserveSeat(seats);
      if (seats === 0) {
        reservationEnabled = false;
      }
      done();
    }
  });

  res.json({ status: 'Queue processing' });
});

// Start the server
app.listen(1245, () => {
  console.log('Server is running on port 1245');
});
