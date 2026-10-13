'use client';

import React, { useState } from 'react';
import Image from 'next/image';
import { siteContent } from '@/data/siteContent';
import { useBooking } from '@/context/BookingContext';
import { Clock, ArrowUpRight } from 'lucide-react';

export default function SalonMenuSection() {
  const { openBooking } = useBooking();
  const [selectedIndex, setSelectedIndex] = useState(0);

  const selectedRitual = siteContent.rituals[selectedIndex];

  return (
    <section id="rituals" className="py-24 lg:py-32 bg-luxe-black text-white relative">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Section Header */}
        <div className="flex flex-col md:flex-row md:items-end justify-between gap-6 mb-16 pb-6 border-b border-zinc-800">
          <div>
            <span className="font-sans text-xs uppercase tracking-[0.25em] text-gold-accent block mb-2 font-medium">
              Salon Menu & Pricing
            </span>
            <h2 className="font-serif text-3xl sm:text-4xl lg:text-5xl font-normal text-white">
              Signature Treatments & Services
            </h2>
          </div>
          <p className="font-serif text-sm sm:text-base text-zinc-400 italic max-w-md">
            “Transparent tariffs in INR. All treatments performed in private soundproof suites with single-use sterile cassettes.”
          </p>
        </div>

        {/* Split Service Showcase */}
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-12 items-start">
          {/* Left: Minimalist Monolithic Ritual List (6 cols) */}
          <div className="lg:col-span-6 space-y-3">
            {siteContent.rituals.map((ritual, idx) => {
              const isSelected = selectedIndex === idx;

              return (
                <div
                  key={ritual.id}
                  onClick={() => setSelectedIndex(idx)}
                  className={`p-6 rounded-sm border transition-all duration-200 cursor-pointer group flex flex-col justify-between ${
                    isSelected
                      ? 'bg-luxe-card border-gold-accent shadow-xl'
                      : 'bg-transparent border-zinc-800/80 hover:border-zinc-700 hover:bg-zinc-900/40'
                  }`}
                >
                  <div className="flex items-baseline justify-between gap-4">
                    <div className="flex items-baseline gap-3">
                      <span className="font-sans text-xs text-gold-accent font-semibold tracking-wider">
                        {ritual.number}
                      </span>
                      <h3
                        className={`font-serif text-xl sm:text-2xl transition-colors ${
                          isSelected
                            ? 'text-white'
                            : 'text-zinc-300 group-hover:text-white'
                        }`}
                      >
                        {ritual.name}
                      </h3>
                    </div>

                    <span className="font-serif text-lg font-medium text-gold-accent shrink-0">
                      {ritual.formattedPrice}
                    </span>
                  </div>

                  {isSelected && (
                    <div className="mt-3 pt-3 border-t border-zinc-800 flex items-center justify-between text-xs text-zinc-400">
                      <span className="font-serif italic text-gold-accent">
                        {ritual.bengaliName}
                      </span>
                      <span className="flex items-center gap-1 font-sans text-xs">
                        <Clock className="w-3 h-3 text-gold-accent" />
                        {ritual.duration}
                      </span>
                    </div>
                  )}
                </div>
              );
            })}
          </div>

          {/* Right: Interactive Visual Canvas (6 cols) */}
          <div className="lg:col-span-6 sticky top-24">
            <div className="p-8 rounded-sm bg-luxe-card border border-gold-500/30 shadow-2xl space-y-6">
              {/* Preloaded Multi-Layer High-Fashion Canvas Image (0ms delay) */}
              <div className="relative aspect-[16/10] w-full rounded-sm overflow-hidden border border-zinc-800 bg-zinc-900">
                {siteContent.rituals.map((ritual, idx) => (
                  <div
                    key={ritual.id}
                    className={`absolute inset-0 transition-opacity duration-500 ease-in-out ${
                      selectedIndex === idx
                        ? 'opacity-100 z-10'
                        : 'opacity-0 z-0 pointer-events-none'
                    }`}
                  >
                    <Image
                      src={ritual.image}
                      alt={ritual.name}
                      fill
                      priority={true}
                      unoptimized
                      className="object-cover"
                      sizes="(max-width: 1024px) 100vw, 50vw"
                    />
                    <div className="absolute inset-0 bg-gradient-to-t from-luxe-card via-transparent to-transparent opacity-80" />
                  </div>
                ))}

                <div className="absolute top-4 left-4 z-20 px-2.5 py-1 bg-luxe-black/80 backdrop-blur-sm border border-gold-500/30 text-[10px] uppercase font-sans tracking-widest text-gold-accent font-medium rounded-xs">
                  {selectedRitual.categoryLabel}
                </div>

                <div className="absolute bottom-4 right-4 z-20 font-serif text-xl font-medium text-white bg-black/80 px-3 py-1 border border-gold-500/30">
                  {selectedRitual.formattedPrice}
                </div>
              </div>

              {/* Ritual Details */}
              <div className="space-y-4">
                <div>
                  <h3 className="font-serif text-2xl font-normal text-white">
                    {selectedRitual.name}
                  </h3>
                  <p className="text-xs text-gold-accent font-serif italic mt-0.5">
                    {selectedRitual.bengaliName} • {selectedRitual.duration}
                  </p>
                  <p className="text-xs text-zinc-300 font-light mt-2 leading-relaxed">
                    {selectedRitual.description}
                  </p>
                </div>

                {/* Botanical Notes Chips */}
                <div className="pt-2">
                  <span className="font-sans text-[10px] uppercase tracking-widest text-zinc-500 block mb-2 font-medium">
                    Key Botanical Notes
                  </span>
                  <div className="flex flex-wrap gap-2">
                    {selectedRitual.botanicalNotes.map((note, idx) => (
                      <span
                        key={idx}
                        className="px-2.5 py-1 text-[11px] font-sans bg-luxe-black border border-zinc-800 text-zinc-300 rounded-xs"
                      >
                        {note}
                      </span>
                    ))}
                  </div>
                </div>

                {/* Direct Reservation Trigger */}
                <div className="pt-4 border-t border-zinc-800">
                  <button
                    type="button"
                    onClick={() => openBooking(selectedRitual)}
                    className="cursor-pointer w-full py-3.5 bg-gradient-to-r from-gold-600 via-gold-500 to-gold-400 hover:from-gold-500 text-luxe-black font-semibold text-xs uppercase tracking-[0.2em] transition-all duration-200 flex items-center justify-center gap-2 shadow-lg shadow-gold-500/10 active:scale-98"
                  >
                    <span>Book This Service</span>
                    <ArrowUpRight className="w-4 h-4" />
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
