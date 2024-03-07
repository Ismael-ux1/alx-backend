// Import necessary modules
import express from 'express';
import redis from 'redis';
import { promisify } from 'util';
import kue from 'kue';

// Create an array of products
const listProducts = [
  { id: 1, name: 'Suitcase 250', price: 50, stock: 4 },
  { id: 2, name: 'Suitcase 450', price: 100, stock: 10 },
  { id: 3, name: 'Suitcase 650', price: 350, stock: 2 },
  { id: 4, name: 'Suitcase 1050', price: 550, stock: 5 },
];

// Function to get a product by its ID
function getItemById(id) {
  return listProducts.find((product) => product.id === id);
}

// Create an Express server
const app = express();

// Route to get all products
app.get('/list_products', (req, res) => {
  res.json(listProducts);
});

// Create a Redis client
const client = redis.createClient();

// Promisify the get and set methods
const getAsync = promisify(client.get).bind(client);
const setAsync = promisify(client.set).bind(client);

// Function to reserve stock by ID
async function reserveStockById(itemId, stock) {
  await setAsync(`item.${itemId}`, stock);
}

// Async function to get current reserved stock by ID
async function getCurrentReservedStockById(itemId) {
  const stock = await getAsync(`item.${itemId}`);
  return stock;
}

// Route to get product detail
app.get('/list_products/:itemId', async (req, res) => {
  const itemId = req.params.itemId;
  const stock = await getCurrentReservedStockById(itemId);

  if (stock === null) {
    res.json({ status: 'Product not found' });
  } else {
    res.json({ itemId, stock });
  }
});

// Route to reserve a product
app.get('/reserve_product/:itemId', async (req, res) => {
  const itemId = req.params.itemId;
  const stock = await getCurrentReservedStockById(itemId);

  if (stock === null) {
    res.json({ status: 'Product not found' });
  } else if (stock < 1) {
    res.json({ status: 'Not enough stock available', itemId });
  } else {
    await reserveStockById(itemId, stock - 1);
    res.json({ status: 'Reservation confirmed', itemId });
  }
});

// Create a queue
const queue = kue.createQueue();

// For each product in listProducts
for (const product of listProducts) {
  // Create a job
  const job = queue.create('push_notification_code_2', product)
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

// Start the server
app.listen(1245, () => {
  console.log('Server is running on port 1245');
});
