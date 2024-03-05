// Import necessary modules
import redis from 'redis';
import { promisify } from 'util';

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

// Promisify the Redis client methods
const asyncGet = promisify(client.get).bind(client);

// Function to set a new school value
function setNewSchool(schoolName, value) {
  client.set(schoolName, value, redis.print);
}

// Async Function to display the value for a school
async function displaySchoolValue(schoolName) {
  try {
    const value = await asyncGet(schoolName); // Use async/await
    console.log(`Value for ${schoolName}:`, value);
  } catch (error) {
    console.error('Error getting value:', error.message);
  }
}

// Call the functions
displaySchoolValue('Holberton');
setNewSchool('HolbertonSanFrancisco', '100');
displaySchoolValue('HolbertonSanFrancisco');
