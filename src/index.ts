import express, { Request, Response } from 'express';
import { SVG, registerWindow } from '@svgdotjs/svg.js';
import { createSVGWindow } from 'svgdom';
import fs from 'fs';
import path from 'path';

const app = express();
const port = process.env.PORT || 3000;

// Setup SVG.js with svgdom to run headlessly in Node
const window = createSVGWindow();
const document = window.document;
registerWindow(window, document);

app.use(express.json());

// Health check
app.get('/', (_req: Request, res: Response) => {
  res.send('🎬 svgvidgen is running');
});

// Render route: dynamically create SVG frame (placeholder content)
app.post('/render', (req: Request, res: Response) => {
  const { width = 800, height = 600, message = "Hello SVG" } = req.body;

  const draw = SVG(document.documentElement).size(width, height);
  draw.rect(width, height).fill('#111');
  draw.text(message).fill('#0ff').font({ size: 48 }).move(50, 50);

  const svgOutput = draw.svg();
  res.setHeader('Content-Type', 'image/svg+xml');
  res.send(svgOutput);
});

// Start server
app.listen(port, () => {
  console.log(`🚀 svgvidgen listening at http://localhost:${port}`);
});
