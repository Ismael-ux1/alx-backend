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
  console.error('Redis client not connected to the server:', err.message);
});
