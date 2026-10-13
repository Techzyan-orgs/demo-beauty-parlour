'use client';

import React, { useState } from 'react';
import Image from 'next/image';
import { siteContent } from '@/data/siteContent';
import { LookbookPhoto } from '@/types';
import { Sparkles, Maximize2, X, Camera } from 'lucide-react';

export default function VisualLookbookGrid() {
  const [activeFilter, setActiveFilter] = useState<string>('All');
  const [activeModalPhoto, setActiveModalPhoto] = useState<LookbookPhoto | null>(null);

  const categories = [
    'All',
    'Bridal Makeup',
    'Skin Glow',
    'Hair Art',
    'Salon Suites',
  ];

  const filteredPhotos =
    activeFilter === 'All'
      ? siteContent.lookbookPhotos
      : siteContent.lookbookPhotos.filter((p) => p.category === activeFilter);

  return (
    <section id="lookbook" className="py-24 lg:py-32 bg-luxe-dark text-white relative">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Minimalist Section Header */}
        <div className="flex flex-col md:flex-row md:items-end justify-between gap-6 mb-12 pb-6 border-b border-zinc-800">
          <div>
            <div className="inline-flex items-center gap-2 text-xs uppercase tracking-[0.25em] text-gold-accent font-sans mb-2">
              <Camera className="w-3.5 h-3.5" />
              <span>Bridal & Beauty Portfolio</span>
            </div>
            <h2 className="font-serif text-3xl sm:text-4xl lg:text-5xl font-normal text-white">
              Client Showcase
            </h2>
          </div>

          {/* Category Filter Pills */}
          <div className="flex flex-wrap gap-2">
            {categories.map((cat) => (
              <button
                key={cat}
                type="button"
                onClick={() => setActiveFilter(cat)}
                className={`cursor-pointer px-3.5 py-1.5 text-xs font-sans tracking-wider rounded-full border transition-all active:scale-95 ${
                  activeFilter === cat
                    ? 'border-gold-accent bg-gold-500/25 text-gold-accent font-semibold shadow-md shadow-gold-500/10'
                    : 'border-zinc-800 bg-luxe-black/60 text-zinc-400 hover:text-white'
                }`}
              >
                {cat}
              </button>
            ))}
          </div>
        </div>

        {/* Dynamic Image Grid - Perfectly aligned uniform 3:4 portrait cards */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 sm:gap-6">
          {filteredPhotos.map((photo, idx) => (
            <div
              key={photo.id}
              onClick={() => setActiveModalPhoto(photo)}
              className="group relative rounded-sm overflow-hidden border border-zinc-800 hover:border-gold-500/50 cursor-pointer bg-zinc-950 transition-all duration-300 shadow-xl aspect-[3/4] w-full"
            >
              <Image
                src={photo.image}
                alt={photo.title}
                fill
                priority={idx < 4}
                unoptimized
                className="object-cover transition-transform duration-700 group-hover:scale-108"
                sizes="(max-width: 768px) 50vw, 25vw"
              />

              {/* Hover Dark Vignette & Caption Reveal */}
              <div className="absolute inset-0 bg-gradient-to-t from-luxe-black/95 via-luxe-black/40 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300 flex flex-col justify-between p-4 z-10">
                <div className="flex justify-end">
                  <span className="p-1.5 rounded-full bg-black/60 border border-gold-500/30 text-gold-accent">
                    <Maximize2 className="w-3.5 h-3.5" />
                  </span>
                </div>

                <div>
                  <span className="font-sans text-[10px] uppercase tracking-widest text-gold-accent block mb-1">
                    {photo.category}
                  </span>
                  <h4 className="font-serif text-sm sm:text-base font-normal text-white">
                    {photo.title}
                  </h4>
                  <p className="text-[11px] text-zinc-300 font-light mt-0.5 line-clamp-2">
                    {photo.caption}
                  </p>
                </div>
              </div>
            </div>
          ))}
        </div>

        {/* Modal Lightbox Zoom */}
        {activeModalPhoto && (
          <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/95 backdrop-blur-md">
            <div className="relative max-w-3xl w-full bg-luxe-card border border-gold-500/40 rounded-sm overflow-hidden shadow-2xl">
              <button
                type="button"
                onClick={() => setActiveModalPhoto(null)}
                className="cursor-pointer absolute top-4 right-4 z-20 p-2 bg-black/80 hover:bg-gold-500 text-white hover:text-black rounded-full transition-colors"
              >
                <X className="w-5 h-5" />
              </button>

              <div className="relative aspect-[4/3] sm:aspect-[16/10] w-full bg-black">
                <Image
                  src={activeModalPhoto.image}
                  alt={activeModalPhoto.title}
                  fill
                  unoptimized
                  className="object-contain"
                />
              </div>

              <div className="p-6 bg-luxe-black/95 border-t border-zinc-800">
                <span className="font-sans text-[11px] uppercase tracking-widest text-gold-accent font-semibold block">
                  {activeModalPhoto.category}
                </span>
                <h3 className="font-serif text-2xl text-white mt-1">
                  {activeModalPhoto.title}
                </h3>
                <p className="text-xs text-zinc-300 font-light mt-1">
                  {activeModalPhoto.caption}
                </p>
              </div>
            </div>
          </div>
        )}
      </div>
    </section>
  );
}
