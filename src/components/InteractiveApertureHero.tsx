'use client';

import React, { useState } from 'react';
import Image from 'next/image';
import { siteContent } from '@/data/siteContent';
import { useBooking } from '@/context/BookingContext';
import { Sparkles, ArrowRight } from 'lucide-react';

export default function InteractiveApertureHero() {
  const { openBooking } = useBooking();
  const [activeEditionIndex, setActiveEditionIndex] = useState(0);

  const activeEdition = siteContent.moodEditions[activeEditionIndex];
  const matchedRitual =
    siteContent.rituals.find((r) => r.id === activeEdition.ritualId) ||
    siteContent.rituals[0];

  return (
    <section
      id="aperture"
      className="relative min-h-[90vh] flex flex-col justify-between overflow-hidden bg-luxe-black text-white select-none"
    >
      {/* Preloaded Multi-Layer Background Cinematic Canvas (0ms network delay on switch) */}
      <div className="absolute inset-0 z-0 overflow-hidden pointer-events-none">
        {siteContent.moodEditions.map((edition, idx) => (
          <div
            key={edition.id}
            className={`absolute inset-0 transition-opacity duration-700 ease-in-out ${
              activeEditionIndex === idx
                ? 'opacity-40 z-10'
                : 'opacity-0 z-0'
            }`}
          >
            <Image
              src={edition.image}
              alt={edition.title}
              fill
              priority={true}
              unoptimized
              className="object-cover object-center"
              sizes="100vw"
            />
          </div>
        ))}
        <div className="absolute inset-0 z-20 bg-gradient-to-t from-luxe-black via-luxe-black/60 to-luxe-black/30" />
        <div className="absolute inset-0 z-20 bg-[radial-gradient(#d4af37_1px,transparent_1px)] [background-size:48px_48px] opacity-[0.03]" />
      </div>

      {/* Top Edition Selector Dial (High z-index, zero click obstruction) */}
      <div className="relative z-30 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 w-full pt-8 sm:pt-12">
        <div className="flex flex-wrap items-center justify-between gap-4 pb-6 border-b border-zinc-800/80">
          <div className="flex items-center gap-3">
            <span className="text-[10px] uppercase tracking-[0.25em] text-gold-accent font-semibold">
              Signature Mood Edition
            </span>
            <span className="text-zinc-600 font-sans text-xs">/</span>
            <span className="font-sans text-xs tracking-wider text-zinc-300">
              {activeEdition.number} of 03
            </span>
          </div>

          {/* Interactive Edition Toggles with Instant Tactile Feedback */}
          <div className="flex items-center gap-2 relative z-40">
            {siteContent.moodEditions.map((edition, idx) => {
              const isActive = activeEditionIndex === idx;
              return (
                <button
                  key={edition.id}
                  type="button"
                  onClick={() => setActiveEditionIndex(idx)}
                  className={`cursor-pointer relative px-3.5 sm:px-4 py-1.5 text-xs font-sans tracking-wider transition-all duration-200 rounded-full border active:scale-95 focus:outline-none ${
                    isActive
                      ? 'border-gold-accent bg-gold-500/25 text-gold-accent font-semibold shadow-md shadow-gold-500/10'
                      : 'border-zinc-800 bg-black/60 text-zinc-400 hover:text-white hover:border-zinc-700'
                  }`}
                >
                  <span className="relative z-10 flex items-center gap-1.5">
                    {isActive && (
                      <span className="w-1.5 h-1.5 rounded-full bg-gold-accent animate-ping" />
                    )}
                    <span>{edition.number} • {edition.title.split(' ')[0]}</span>
                  </span>
                </button>
              );
            })}
          </div>
        </div>
      </div>

      {/* Main Aperture Stage: Asymmetric Typographic Masterpiece */}
      <div className="relative z-20 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 w-full py-12 lg:py-16 my-auto">
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-end">
          {/* Left Hero Title & Bengali Poetry */}
          <div className="lg:col-span-8 space-y-4">
            <div className="inline-flex items-center gap-2 text-gold-accent text-xs tracking-[0.3em] uppercase">
              <Sparkles className="w-3.5 h-3.5" />
              <span>{activeEdition.concept}</span>
            </div>

            <div className="flex flex-col">
              <h1 className="font-serif text-5xl sm:text-6xl md:text-7xl xl:text-8xl font-normal tracking-tight text-white leading-none transition-all duration-300">
                {activeEdition.title}
              </h1>
              <span className="font-serif text-2xl sm:text-3xl text-gold-accent italic mt-2 opacity-90 transition-all duration-300">
                {activeEdition.bengaliTitle}
              </span>
            </div>

            <p className="font-serif text-base sm:text-lg text-zinc-300 italic max-w-xl pt-2 transition-all duration-300">
              {activeEdition.quote}
            </p>
          </div>

          {/* Right Action & Ritual Card */}
          <div className="lg:col-span-4 p-6 rounded-sm bg-luxe-card/90 border border-gold-500/30 backdrop-blur-md space-y-4 shadow-2xl relative z-20">
            <div className="flex items-center justify-between text-xs text-zinc-400 border-b border-zinc-800 pb-3">
              <span className="uppercase tracking-widest text-[10px]">Aesthetic Palette</span>
              <span className="text-zinc-200 font-sans text-xs tracking-wide">{activeEdition.paletteDescription}</span>
            </div>

            <div>
              <span className="text-[10px] uppercase tracking-widest text-gold-accent font-semibold block">
                Featured Ritual
              </span>
              <h3 className="font-serif text-lg text-white mt-0.5">
                {matchedRitual.name}
              </h3>
              <p className="text-xs text-zinc-400 mt-1">
                {matchedRitual.formattedPrice} • {matchedRitual.duration}
              </p>
            </div>

            <button
              type="button"
              onClick={() => openBooking(matchedRitual)}
              className="cursor-pointer w-full py-3 bg-gradient-to-r from-gold-600 via-gold-500 to-gold-400 hover:from-gold-500 hover:to-gold-300 text-luxe-black font-semibold text-xs uppercase tracking-[0.2em] transition-all duration-200 flex items-center justify-center gap-2 group shadow-lg shadow-gold-500/10 active:scale-98"
            >
              <span>Experience This Look</span>
              <ArrowRight className="w-3.5 h-3.5 transition-transform group-hover:translate-x-1" />
            </button>
          </div>
        </div>
      </div>

      {/* Bottom Editorial Marquee Ticker */}
      <div className="relative z-20 border-t border-zinc-800/80 bg-luxe-black/95 py-3 overflow-hidden">
        <div className="flex whitespace-nowrap animate-marquee text-[11px] uppercase tracking-[0.25em] text-zinc-400 font-sans gap-8">
          <span>{siteContent.contact.address}</span>
          <span className="text-gold-accent">•</span>
          <span>100% Autoclaved Medical Hygiene</span>
          <span className="text-gold-accent">•</span>
          <span>Darjeeling Single-Estate Tea Service</span>
          <span className="text-gold-accent">•</span>
          <span>Private Acoustic Suites</span>
          <span className="text-gold-accent">•</span>
          <span>{siteContent.contact.address}</span>
          <span className="text-gold-accent">•</span>
          <span>100% Autoclaved Medical Hygiene</span>
        </div>
      </div>
    </section>
  );
}
