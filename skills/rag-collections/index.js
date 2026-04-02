#!/usr/bin/env node

const axios = require('axios');
const fs = require('fs');
const FormData = require('form-data');
const path = require('path');

// Base configuration
const BASE_URL = 'http://100.84.93.86:8000';
const axiosInstance = axios.create({
  baseURL: BASE_URL,
  timeout: 30000,
});

/**
 * Health Check
 */
async function healthCheck() {
  try {
    const response = await axiosInstance.get('/api/v1/health');
    console.log('Health check successful:', response.data);
    return response.data;
  } catch (error) {
    console.error('Health check failed:', error.message);
    throw error;
  }
}

/**
 * Get System Metrics
 */
async function getMetrics() {
  try {
    const response = await axiosInstance.get('/api/v1/metrics');
    console.log('System metrics:', response.data);
    return response.data;
  } catch (error) {
    console.error('Failed to get metrics:', error.message);
    throw error;
  }
}

/**
 * Collection Management
 */

/**
 * Create a new collection
 * @param {string} name - Unique collection name
 * @param {string} [description] - Collection description
 * @param {object} [metadata] - Arbitrary metadata
 */
async function createCollection(name, description = '', metadata = {}) {
  try {
    const response = await axios