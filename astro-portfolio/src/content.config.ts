import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

const blog = defineCollection({
  loader: glob({ pattern: "blog/**\/*.mdx", base: "src/content", generateId: ({ entry }) => entry.replace(/\.mdx$/, "").replace(/^blog\//, "") }),
  schema: z.object({
    title: z.string(),
    description: z.string(),
    pubDate: z.date(),
    updatedDate: z.date().optional(),
    heroImage: z.string().optional(),
    tags: z.array(z.string()).default([]),
    author: z.string().default('Jonathan Esteban'),
    draft: z.boolean().default(false),
  }),
});

export const collections = { blog };