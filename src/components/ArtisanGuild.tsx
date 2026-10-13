'use client';

import React from 'react';
import Image from 'next/image';
import { siteContent } from '@/data/siteContent';
import { useBooking } from '@/context/BookingContext';
import { Star, ArrowUpRight } from 'lucide-react';

export default function ArtisanGuild() {
  const { openBooking } = useBooking();

  return (
    <section id="artisans" className="py-24 lg:py-32 bg-luxe-black text-white relative">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Section Header */}
        <div className="flex flex-col md:flex-row md:items-end justify-between gap-6 mb-16 pb-6 border-b border-zinc-800">
          <div>
            <span className="font-sans text-xs uppercase tracking-[0.25em] text-gold-accent block mb-2 font-medium">
              Our Team
            </span>
            <h2 className="font-serif text-3xl sm:text-4xl lg:text-5xl font-normal text-white">
              Senior Stylists & Artists
            </h2>
          </div>
          <p className="font-serif text-sm sm:text-base text-zinc-400 italic max-w-md">
            “Every appointment is conducted directly by our senior specialists and artists.”
          </p>
        </div>

        {/* 3 Master Artisans Lineup */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {siteContent.artisans.map((artisan) => (
            <div
              key={artisan.id}
              className="group flex flex-col bg-luxe-card border border-zinc-800 hover:border-gold-500/40 rounded-sm overflow-hidden transition-all duration-300"
            >
              {/* Portrait */}
              <div className="relative aspect-[3/4] w-full overflow-hidden bg-zinc-900">
                <Image
                  src={artisan.image}
                  alt={artisan.name}
                  fill
                  className="object-cover transition-transform duration-700 group-hover:scale-105"
                  sizes="(max-width: 768px) 100vw, 33vw"
                />
                <div className="absolute inset-0 bg-gradient-to-t from-luxe-card via-transparent to-transparent opacity-90" />

                <div className="absolute top-4 left-4 px-2.5 py-1 bg-black/80 backdrop-blur-sm border border-gold-500/30 text-[10px] font-sans font-medium text-gold-accent flex items-center gap-1">
                  <Star className="w-3 h-3 fill-gold-accent" />
                  <span>{artisan.rating}</span>
                </div>

                <div className="absolute bottom-4 left-4 right-4 text-xs text-zinc-300 font-serif italic">
                  {artisan.philosophy}
                </div>
              </div>

              {/* Details */}
              <div className="p-6 flex flex-col flex-grow justify-between space-y-4">
                <div>
                  <h3 className="font-serif text-2xl font-normal text-white">
                    {artisan.name}
                  </h3>
                  <p className="text-xs text-gold-accent font-sans tracking-wide font-medium mt-0.5">
                    {artisan.role} • {artisan.experience}
                  </p>
                  <p className="text-xs text-zinc-400 font-light mt-2">
                    {artisan.speciality}
                  </p>

                  <div className="mt-4 pt-3 border-t border-zinc-800 space-y-1">
                    {artisan.credentials.map((cred, idx) => (
                      <div key={idx} className="text-xs font-sans text-zinc-400 font-light">
                        • {cred}
                      </div>
                    ))}
                  </div>
                </div>

                <div className="pt-2">
                  <button
                    onClick={() => openBooking()}
                    className="w-full py-2.5 bg-luxe-muted hover:bg-gold-500 hover:text-luxe-black text-gold-accent border border-gold-500/30 text-xs font-sans uppercase tracking-wider font-medium transition-colors flex items-center justify-center gap-1.5 cursor-pointer"
                  >
                    <span>Book with Stylist</span>
                    <ArrowUpRight className="w-3.5 h-3.5" />
                  </button>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
