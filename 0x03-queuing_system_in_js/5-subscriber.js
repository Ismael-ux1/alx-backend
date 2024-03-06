// Import necessary modules
import redis from 'redis';

// Create a Redis client
const client = redis.createClient({
  host: 'localhost',
  port: 6379,
});

// Connect to Redis
client.on('connect', () => {
  console.log('Redis client connected to the server');
});

// Handle connection errors
client.on('error', (err) => {
  console.error(`Redis client not connected to the server: ${err.message}`);
});

// Subscribe to the channel
client.subscribe('holberton school channel');

// Handle messages
client.on('message', (channel, message) => {
  console.log(message);

  // If the message is 'KILL_SERVER', unsubscribe and quit
  if (message === 'KILL_SERVER') {
    client.unsubscribe();
    client.quit();
  }
});
