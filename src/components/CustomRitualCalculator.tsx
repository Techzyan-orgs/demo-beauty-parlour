'use client';

import React, { useState } from 'react';
import { siteContent } from '@/data/siteContent';
import { useBooking } from '@/context/BookingContext';
import { Calculator, Check, Plus, Clock, Sparkles, ArrowRight, RotateCcw } from 'lucide-react';

export default function CustomRitualCalculator() {
  const { openBooking } = useBooking();
  const [selectedIds, setSelectedIds] = useState<string[]>([
    'calc-chandan',
    'calc-gold-facial',
  ]);

  const toggleItem = (id: string) => {
    setSelectedIds((prev) =>
      prev.includes(id) ? prev.filter((item) => item !== id) : [...prev, id]
    );
  };

  const resetSelection = () => {
    setSelectedIds(['calc-chandan', 'calc-gold-facial']);
  };

  // Calculations
  const selectedItems = siteContent.calculatorItems.filter((item) =>
    selectedIds.includes(item.id)
  );

  const totalPrice = selectedItems.reduce((acc, curr) => acc + curr.price, 0);
  const totalMinutes = selectedItems.reduce(
    (acc, curr) => acc + curr.durationMinutes,
    0
  );

  const formattedHours = `${Math.floor(totalMinutes / 60)}h ${
    totalMinutes % 60 ? `${totalMinutes % 60}m` : ''
  }`.trim();

  const formattedTotalPrice = `₹${totalPrice.toLocaleString('en-IN')}`;

  return (
    <section id="calculator" className="py-24 lg:py-32 bg-luxe-black text-white relative">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Section Header */}
        <div className="flex flex-col md:flex-row md:items-end justify-between gap-6 mb-12 pb-6 border-b border-zinc-800">
          <div>
            <div className="inline-flex items-center gap-2 text-xs uppercase tracking-[0.25em] text-gold-accent font-sans mb-2">
              <Calculator className="w-3.5 h-3.5" />
              <span>Custom Package Estimator</span>
            </div>
            <h2 className="font-serif text-3xl sm:text-4xl lg:text-5xl font-normal text-white">
              Calculate Your Package & Pricing
            </h2>
          </div>
          <p className="font-serif text-sm text-zinc-400 italic max-w-sm">
            “Select desired treatments to calculate service duration and total price.”
          </p>
        </div>

        {/* Interactive Grid & Live Estimator Terminal */}
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
          {/* Left: 8 Selectable Ritual Cards (8 cols) */}
          <div className="lg:col-span-8 grid grid-cols-1 sm:grid-cols-2 gap-3.5">
            {siteContent.calculatorItems.map((item) => {
              const isSelected = selectedIds.includes(item.id);
              return (
                <div
                  key={item.id}
                  onClick={() => toggleItem(item.id)}
                  className={`p-4 rounded-sm border transition-all duration-200 cursor-pointer flex flex-col justify-between gap-3 ${
                    isSelected
                      ? 'bg-luxe-card border-gold-accent shadow-lg shadow-gold-500/5'
                      : 'bg-luxe-dark/40 border-zinc-800/80 hover:border-zinc-700'
                  }`}
                >
                  <div className="flex items-start justify-between gap-2">
                    <div>
                      <span className="font-sans text-[10px] uppercase tracking-widest text-zinc-400 block mb-0.5 font-medium">
                        {item.category}
                      </span>
                      <h4 className="font-serif text-base font-normal text-white leading-snug">
                        {item.name}
                      </h4>
                    </div>

                    <div
                      className={`w-6 h-6 rounded-full flex items-center justify-center shrink-0 transition-colors ${
                        isSelected
                          ? 'bg-gold-500 text-black'
                          : 'bg-zinc-800 text-zinc-500'
                      }`}
                    >
                      {isSelected ? <Check className="w-3.5 h-3.5 stroke-[3]" /> : <Plus className="w-3.5 h-3.5" />}
                    </div>
                  </div>

                  <div className="flex items-center justify-between pt-2 border-t border-zinc-800/60 font-sans text-xs">
                    <span className="text-zinc-400 flex items-center gap-1 text-[11px]">
                      <Clock className="w-3 h-3 text-gold-accent" />
                      {item.duration}
                    </span>
                    <span className="font-serif text-sm font-medium text-gold-accent">
                      {item.formattedPrice}
                    </span>
                  </div>
                </div>
              );
            })}
          </div>

          {/* Right: Sticky Live Estimator Docket (4 cols) */}
          <div className="lg:col-span-4 sticky top-24">
            <div className="p-6 rounded-sm bg-luxe-card border border-gold-500/40 shadow-2xl space-y-6">
              <div className="flex items-center justify-between pb-3 border-b border-zinc-800">
                <span className="font-sans text-[11px] uppercase tracking-[0.2em] text-gold-accent font-semibold">
                  Estimated Total
                </span>
                <button
                  onClick={resetSelection}
                  className="font-sans text-[11px] text-zinc-400 hover:text-gold-accent flex items-center gap-1 tracking-wide"
                  title="Reset to default"
                >
                  <RotateCcw className="w-3 h-3" />
                  <span>Reset</span>
                </button>
              </div>

              {/* Selected List Chips */}
              <div className="space-y-2 max-h-48 overflow-y-auto pr-1">
                {selectedItems.length === 0 ? (
                  <p className="text-xs text-zinc-500 italic py-4 text-center">
                    No services selected. Click any service above to add.
                  </p>
                ) : (
                  selectedItems.map((item) => (
                    <div
                      key={item.id}
                      className="flex items-center justify-between text-xs font-sans py-1.5 border-b border-zinc-800/40"
                    >
                      <span className="text-zinc-300 truncate max-w-[170px]">{item.name}</span>
                      <span className="text-gold-accent font-medium">{item.formattedPrice}</span>
                    </div>
                  ))
                )}
              </div>

              {/* Totals Summary */}
              <div className="pt-4 border-t border-zinc-800 space-y-2.5">
                <div className="flex justify-between items-baseline font-sans text-xs">
                  <span className="text-zinc-400">Total Duration:</span>
                  <span className="text-white font-medium">{formattedHours || '0h'}</span>
                </div>
                <div className="flex justify-between items-baseline font-sans text-xs">
                  <span className="text-zinc-400">Selected Services:</span>
                  <span className="text-white">{selectedItems.length} Services</span>
                </div>
                <div className="flex justify-between items-baseline pt-2 border-t border-zinc-800">
                  <span className="font-sans text-xs uppercase tracking-wider text-zinc-400 font-medium">
                    Estimated Price:
                  </span>
                  <span className="font-serif text-2xl font-normal text-gold-gradient">
                    {formattedTotalPrice}
                  </span>
                </div>
              </div>

              {/* Action Button */}
              <button
                type="button"
                onClick={() => openBooking()}
                disabled={selectedItems.length === 0}
                className="w-full py-3.5 bg-gradient-to-r from-gold-600 via-gold-500 to-gold-400 hover:from-gold-500 disabled:opacity-50 text-luxe-black font-semibold text-xs uppercase tracking-[0.2em] transition-all duration-200 flex items-center justify-center gap-2 shadow-lg shadow-gold-500/10 cursor-pointer active:scale-98"
              >
                <span>Book This Package</span>
                <ArrowRight className="w-4 h-4" />
              </button>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
