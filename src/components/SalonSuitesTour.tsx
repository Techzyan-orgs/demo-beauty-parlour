'use client';

import React, { useState } from 'react';
import Image from 'next/image';
import { siteContent } from '@/data/siteContent';
import { Compass } from 'lucide-react';

export default function SalonSuitesTour() {
  const [activeSuiteIndex, setActiveSuiteIndex] = useState(0);

  const activeSuite = siteContent.salonSuites[activeSuiteIndex];

  return (
    <section id="suites" className="py-16 sm:py-24 lg:py-32 bg-luxe-dark text-white relative select-none">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Minimalist Section Header */}
        <div className="flex flex-col md:flex-row md:items-end justify-between gap-6 mb-8 sm:mb-12 pb-6 border-b border-zinc-800">
          <div>
            <div className="inline-flex items-center gap-2 text-xs uppercase tracking-[0.25em] text-gold-accent font-sans mb-2">
              <Compass className="w-3.5 h-3.5" />
              <span>Salon Suites</span>
            </div>
            <h2 className="font-serif text-2xl sm:text-4xl lg:text-5xl font-normal text-white">
              The Ballygunge Estate Suites
            </h2>
          </div>

          {/* Interactive Suite Selectors: Symmetrical 2x2 grid on mobile, flex row on desktop */}
          <div className="grid grid-cols-2 sm:flex sm:flex-wrap gap-2 w-full md:w-auto">
            {siteContent.salonSuites.map((suite, idx) => {
              const isActive = activeSuiteIndex === idx;
              return (
                <button
                  key={suite.id}
                  type="button"
                  onClick={() => setActiveSuiteIndex(idx)}
                  className={`cursor-pointer px-3 sm:px-4 py-2 text-center text-xs font-sans tracking-wider rounded-full border transition-all active:scale-95 ${
                    isActive
                      ? 'border-gold-accent bg-gold-500/25 text-gold-accent font-semibold shadow-md shadow-gold-500/10'
                      : 'border-zinc-800 bg-black/60 text-zinc-400 hover:text-white'
                  }`}
                >
                  {suite.number} • {suite.name.split(' ')[1]}
                </button>
              );
            })}
          </div>
        </div>

        {/* Large Visual Showcase Canvas */}
        <div className="w-full rounded-sm overflow-hidden border border-gold-500/30 shadow-2xl bg-zinc-950 relative">
          {/* Photo frame: aspect-[16/10] on mobile so the photo is spacious and unobstructed, 21/9 on desktop */}
          <div className="relative aspect-[16/10] sm:aspect-[16/9] md:aspect-[21/9] w-full overflow-hidden bg-zinc-950">
            {siteContent.salonSuites.map((suite, idx) => (
              <div
                key={suite.id}
                className={`absolute inset-0 transition-opacity duration-700 ease-in-out ${
                  activeSuiteIndex === idx
                    ? 'opacity-85 z-10'
                    : 'opacity-0 z-0 pointer-events-none'
                }`}
              >
                <Image
                  src={suite.image}
                  alt={suite.name}
                  fill
                  priority={true}
                  unoptimized
                  className="object-cover"
                  sizes="(max-width: 1280px) 100vw, 1280px"
                />
                <div className="absolute inset-0 bg-gradient-to-t from-luxe-black via-luxe-black/30 to-transparent" />
              </div>
            ))}

            {/* Mobile Suite Number indicator on photo */}
            <div className="md:hidden absolute top-3 left-3 z-20 px-2.5 py-1 text-[10px] uppercase font-sans tracking-widest text-gold-accent bg-black/80 backdrop-blur-md border border-gold-500/30 rounded-xs">
              Suite {activeSuite.number}
            </div>
          </div>

          {/* Suite Detail Panel: Docked naturally below image on mobile, floating overlay on desktop */}
          <div className="relative md:absolute md:bottom-6 md:left-6 md:right-6 z-20 flex flex-col md:flex-row md:items-end justify-between gap-4 p-5 sm:p-6 bg-luxe-black md:bg-luxe-black/85 md:backdrop-blur-md border-t md:border border-gold-500/30 md:rounded-sm">
            <div>
              <span className="text-[10px] uppercase font-sans tracking-widest text-gold-accent font-semibold block">
                Suite {activeSuite.number} • {activeSuite.bengaliName}
              </span>
              <h3 className="font-serif text-xl sm:text-2xl md:text-3xl text-white mt-1">
                {activeSuite.name}
              </h3>
              <p className="text-xs sm:text-sm text-zinc-300 font-light mt-1.5 max-w-xl leading-relaxed">
                {activeSuite.atmosphere}
              </p>
            </div>

            {/* Hotspot architectural chips */}
            <div className="flex flex-wrap gap-1.5 sm:gap-2 shrink-0 pt-2 md:pt-0">
              {activeSuite.hotspots.map((spot, i) => (
                <span
                  key={i}
                  className="px-2.5 py-1 text-[10px] font-sans uppercase tracking-wider bg-luxe-card border border-gold-500/30 text-gold-accent rounded-xs"
                >
                  ✦ {spot}
                </span>
              ))}
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
