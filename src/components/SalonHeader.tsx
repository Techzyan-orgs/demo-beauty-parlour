'use client';

import React, { useState } from 'react';
import { siteContent } from '@/data/siteContent';
import { useTheme } from '@/context/ThemeContext';
import { useBooking } from '@/context/BookingContext';
import { Volume2, VolumeX, Sparkles, Sun, Moon, ArrowUpRight } from 'lucide-react';

export default function SalonHeader() {
  const { theme, toggleTheme } = useTheme();
  const { openBooking } = useBooking();
  const [isPlayingAudio, setIsPlayingAudio] = useState(false);

  return (
    <header className="sticky top-0 z-50 transition-all duration-300 bg-luxe-black/90 dark:bg-luxe-black/90 bg-zinc-50/90 backdrop-blur-md border-b border-zinc-800/80 dark:border-zinc-800/80 border-zinc-200">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-3.5 flex items-center justify-between">
        {/* Left: Soundscape & Coordinates Ticker */}
        <div className="flex items-center gap-4 text-[11px] tracking-widest text-zinc-400">
          <button
            onClick={() => setIsPlayingAudio(!isPlayingAudio)}
            className="hidden md:flex items-center gap-2 hover:text-gold-accent transition-colors group"
            title="Toggle Ambient Soundscape"
          >
            {isPlayingAudio ? (
              <span className="flex items-center gap-1.5 text-gold-accent">
                <Volume2 className="w-3.5 h-3.5 animate-pulse" />
                <span className="flex gap-0.5 items-end h-2.5">
                  <span className="w-0.5 h-2 bg-gold-accent animate-bounce" />
                  <span className="w-0.5 h-3 bg-gold-accent animate-bounce delay-75" />
                  <span className="w-0.5 h-1.5 bg-gold-accent animate-bounce delay-150" />
                </span>
                <span>Darjeeling Rains</span>
              </span>
            ) : (
              <span className="flex items-center gap-1.5 group-hover:text-gold-accent">
                <VolumeX className="w-3.5 h-3.5" />
                <span>Ambient: Muted</span>
              </span>
            )}
          </button>

          <span className="hidden lg:inline text-zinc-600">/</span>

          <span className="hidden lg:inline font-sans text-[11px] tracking-wider text-zinc-400">
            {siteContent.brand.coordinates}
          </span>
        </div>

        {/* Center: Monolithic Brandmark with Bengali Ligature */}
        <a href="#" className="flex items-center gap-2.5 group">
          <span className="font-serif text-2xl sm:text-3xl font-normal tracking-wide text-white dark:text-white text-zinc-900 group-hover:text-gold-accent transition-colors">
            {siteContent.brand.name}
          </span>
          <span className="font-serif text-base text-gold-accent italic opacity-85">
            {siteContent.brand.bengaliName}
          </span>
        </a>

        {/* Right: Theme Dial & Booking Trigger */}
        <div className="flex items-center gap-3 sm:gap-4">
          <button
            onClick={toggleTheme}
            aria-label="Toggle theme mode"
            className="p-2 rounded-full border border-zinc-700/60 dark:border-zinc-800 text-zinc-300 dark:text-zinc-300 text-zinc-700 hover:text-gold-accent hover:border-gold-accent/50 transition-colors"
          >
            {theme === 'dark' ? (
              <Sun className="w-3.5 h-3.5 text-gold-accent" />
            ) : (
              <Moon className="w-3.5 h-3.5 text-zinc-700" />
            )}
          </button>

          <button
            onClick={() => openBooking()}
            className="px-4 sm:px-5 py-2 rounded-full bg-gold-500 text-luxe-black font-semibold text-[11px] tracking-[0.16em] uppercase hover:bg-gold-400 transition-all duration-300 flex items-center gap-1.5 shadow-md shadow-gold-500/10 active:scale-95"
          >
            <span>Book Appointment</span>
            <ArrowUpRight className="w-3.5 h-3.5" />
          </button>
        </div>
      </div>
    </header>
  );
}
