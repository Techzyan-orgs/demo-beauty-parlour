'use client';

import React, { useState } from 'react';
import Image from 'next/image';
import { siteContent } from '@/data/siteContent';
import { Sparkles, MoveHorizontal } from 'lucide-react';

export default function TransformationLens() {
  const [sliderPosition, setSliderPosition] = useState(50);
  const [activeCaseIndex, setActiveCaseIndex] = useState(0);

  const activeCase = siteContent.transformations[activeCaseIndex];

  const handleSliderChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setSliderPosition(Number(e.target.value));
  };

  return (
    <section id="transformations" className="py-24 lg:py-32 bg-luxe-dark text-white relative overflow-hidden select-none">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Section Header */}
        <div className="text-center max-w-3xl mx-auto mb-16">
          <div className="inline-flex items-center gap-2 text-xs uppercase tracking-[0.25em] text-gold-accent font-sans mb-3">
            <Sparkles className="w-3.5 h-3.5" />
            <span>Before & After</span>
          </div>
          <h2 className="font-serif text-3xl sm:text-4xl lg:text-5xl font-normal text-white">
            Real Client Transformations
          </h2>
          <p className="font-serif text-sm sm:text-base text-zinc-400 italic mt-3">
            “Drag the interactive slider to view the transformation in identical pose.”
          </p>

          {/* Case Toggle Buttons */}
          <div className="mt-6 flex items-center justify-center gap-3">
            {siteContent.transformations.map((item, idx) => (
              <button
                key={item.id}
                type="button"
                onClick={() => setActiveCaseIndex(idx)}
                className={`cursor-pointer px-4 py-2 text-xs font-sans tracking-wider rounded-full border transition-all active:scale-95 ${
                  activeCaseIndex === idx
                    ? 'border-gold-accent bg-gold-500/20 text-gold-accent font-semibold shadow-md shadow-gold-500/10'
                    : 'border-zinc-800 bg-luxe-black text-zinc-400 hover:text-white'
                }`}
              >
                Case 0{idx + 1}: {item.title}
              </button>
            ))}
          </div>
        </div>

        {/* Interactive Drag Reveal Canvas */}
        <div className="max-w-4xl mx-auto">
          <div className="relative aspect-[16/10] sm:aspect-[16/9] w-full rounded-sm overflow-hidden border border-gold-500/40 shadow-2xl">
            {/* Background Image: The "After" (Couture Result) */}
            <Image
              src={activeCase.imageAfter}
              alt={`${activeCase.title} - After Couture`}
              fill
              unoptimized
              priority
              className="object-cover pointer-events-none select-none"
              sizes="(max-width: 1024px) 100vw, 896px"
            />

            {/* Foreground Clipped Image: The "Before" (Initial Canvas) - Exact pixel alignment */}
            <div
              className="absolute inset-0 overflow-hidden pointer-events-none select-none"
              style={{ clipPath: `inset(0 ${100 - sliderPosition}% 0 0)` }}
            >
              <Image
                src={activeCase.imageBefore}
                alt={`${activeCase.title} - Initial Canvas`}
                fill
                unoptimized
                priority
                className="object-cover pointer-events-none select-none"
                sizes="(max-width: 1024px) 100vw, 896px"
              />
            </div>

            {/* Visual Divider Line & Handle */}
            <div
              className="absolute top-0 bottom-0 w-0.5 bg-gold-accent shadow-[0_0_12px_rgba(212,175,55,0.8)] z-20 pointer-events-none"
              style={{ left: `${sliderPosition}%` }}
            >
              <div className="absolute top-1/2 -translate-y-1/2 -translate-x-1/2 w-9 h-9 rounded-full bg-luxe-black border-2 border-gold-accent flex items-center justify-center text-gold-accent shadow-xl">
                <MoveHorizontal className="w-4 h-4" />
              </div>
            </div>

            {/* Labels overlay */}
            <div className="absolute top-4 left-4 z-20 px-3 py-1 bg-black/80 backdrop-blur-sm border border-zinc-700 text-[10px] font-sans tracking-widest uppercase text-zinc-300">
              Before
            </div>
            <div className="absolute top-4 right-4 z-20 px-3 py-1 bg-black/80 backdrop-blur-sm border border-gold-500/40 text-[10px] font-sans tracking-widest uppercase text-gold-accent font-semibold">
              After
            </div>

            {/* Native Range Input for Tactile Dragging */}
            <input
              type="range"
              min="0"
              max="100"
              value={sliderPosition}
              onChange={handleSliderChange}
              aria-label="Comparison slider"
              className="absolute inset-0 w-full h-full opacity-0 cursor-ew-resize z-30"
            />
          </div>

          {/* Caption Note */}
          <div className="mt-4 p-4 rounded-sm bg-luxe-card border border-zinc-800 text-xs text-zinc-400 font-light flex items-center justify-between">
            <span>
              <strong className="text-white font-medium">{activeCase.title}:</strong>{' '}
              {activeCase.notes}
            </span>
            <span className="font-sans text-gold-accent text-xs tracking-wider shrink-0 ml-4">
              {sliderPosition}% Revealed
            </span>
          </div>
        </div>
      </div>
    </section>
  );
}
