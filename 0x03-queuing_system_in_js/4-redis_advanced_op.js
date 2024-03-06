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

// Create a hash
client.hset('HolbertonSchools', 'Portland', '50', redis.print);
client.hset('HolbertonSchools', 'Seattle', '80', redis.print);
client.hset('HolbertonSchools', 'New York', '20', redis.print);
client.hset('HolbertonSchools', 'Bogota', '20', redis.print);
client.hset('HolbertonSchools', 'Cali', '40', redis.print);
client.hset('HolbertonSchools', 'Paris', '2', redis.print);

// Display the hash
client.hgetall('HolbertonSchools', (err, object) => {
  if (err) {
    console.error('Error getting hash:', err.message);
  } else {
    console.log(object);
  }
});
