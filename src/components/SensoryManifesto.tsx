'use client';

import React, { useState } from 'react';
import { siteContent } from '@/data/siteContent';
import { Sparkles, Flower2, Gem, VolumeX } from 'lucide-react';

export default function SensoryManifesto() {
  const [activeDimension, setActiveDimension] = useState(0);

  const icons = [Flower2, Gem, VolumeX];

  return (
    <section id="sensory" className="py-24 lg:py-32 bg-luxe-dark text-white relative overflow-hidden">
      {/* Subtle radial ambience */}
      <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[600px] bg-gold-500/5 rounded-full blur-[140px] pointer-events-none" />

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10">
        {/* Monolithic Editorial Manifesto */}
        <div className="max-w-4xl mx-auto text-center space-y-6 mb-20">
          <div className="inline-flex items-center gap-2 text-xs uppercase tracking-[0.25em] text-gold-accent font-sans">
            <Sparkles className="w-3.5 h-3.5" />
            <span>The Ballygunge Manifesto</span>
          </div>

          <h2 className="font-serif text-3xl sm:text-4xl md:text-5xl lg:text-6xl font-normal text-white leading-tight">
            “{siteContent.manifesto.statement}”
          </h2>

          <p className="font-sans text-sm sm:text-base text-zinc-400 font-light max-w-2xl mx-auto tracking-wide">
            {siteContent.manifesto.subStatement}
          </p>
        </div>

        {/* 3 Interactive Sensory Nodes */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {siteContent.sensoryAlchemies.map((item, idx) => {
            const Icon = icons[idx] || Sparkles;
            const isActive = activeDimension === idx;

            return (
              <div
                key={item.dimension}
                onClick={() => setActiveDimension(idx)}
                className={`p-8 rounded-sm border transition-all duration-300 cursor-pointer flex flex-col justify-between space-y-6 ${
                  isActive
                    ? 'bg-luxe-card border-gold-accent shadow-2xl shadow-gold-500/5'
                    : 'bg-luxe-black/40 border-zinc-800 hover:border-gold-500/40'
                }`}
              >
                <div className="flex items-center justify-between">
                  <span className="font-sans text-xs uppercase tracking-widest text-gold-accent font-medium">
                    Dimension 0{idx + 1}
                  </span>
                  <div className={`p-2 rounded-full ${isActive ? 'bg-gold-500 text-black' : 'bg-zinc-800 text-zinc-400'}`}>
                    <Icon className="w-4 h-4" />
                  </div>
                </div>

                <div className="space-y-2">
                  <h3 className="font-serif text-2xl font-normal text-white">
                    {item.dimension}: {item.element}
                  </h3>
                  <span className="text-xs text-gold-accent font-serif italic block">
                    {item.origin}
                  </span>
                  <p className="text-xs text-zinc-400 font-light leading-relaxed pt-2">
                    {item.description}
                  </p>
                </div>

                <div className="pt-2 border-t border-zinc-800/80 flex items-center justify-between text-[11px] font-sans tracking-wide text-zinc-400">
                  <span>Botanical Grade</span>
                  <span className="text-zinc-300 font-medium">Certified Organic</span>
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </section>
  );
}
