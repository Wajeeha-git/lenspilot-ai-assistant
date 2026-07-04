---
title: FAQ - Technical
category: FAQ
audience: public
source: LensPilot Knowledge Base v1
version: 2026-07-03
public: true
---
# FAQ - Technical

> Some answers below are marked "Not yet confirmed" rather than guessed --
> see FAQ - General for why.

## Which AI model is used?
LensPilot's computer vision uses U-Net and Mask R-CNN models for iris
segmentation.

## How is iris segmentation done?
In real time, using computer vision models (U-Net, Mask R-CNN) built with
OpenCV and PyTorch, to detect and isolate the iris in the camera feed so
lens colors can be accurately overlaid.

## Why is segmentation important?
Accurate iris segmentation is what makes the lens overlay line up
correctly with the customer's actual eyes.

## What happens if lighting is poor?
Not yet confirmed how the system behaves in low light. If try-on quality
seems off, trying better lighting is a reasonable first step, but this
isn't officially documented behavior -- contact support if it persists.

## Why isn't my camera working?
See the Error Handling document.

## Which browsers are supported?
Not yet confirmed. Please contact LensPilot support.
