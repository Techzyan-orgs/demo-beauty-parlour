'use client';

import React, { useState, useEffect } from 'react';
import { siteContent } from '@/data/siteContent';
import { useBooking } from '@/context/BookingContext';
import {
  X,
  CheckCircle2,
  Sparkles,
  Calendar,
  Clock,
  ArrowRight,
  ShieldCheck,
} from 'lucide-react';
import WhatsAppIcon from '@/components/WhatsAppIcon';

export default function BookingModal() {
  const { isBookingOpen, closeBooking, selectedService } = useBooking();

  const [ritualId, setRitualId] = useState<string>(siteContent.rituals[0].id);
  const [artisanId, setArtisanId] = useState<string>(siteContent.artisans[0].id);
  const [date, setDate] = useState<string>('');
  const [timeSlot, setTimeSlot] = useState<string>(siteContent.bookingSlots[0]);
  const [name, setName] = useState<string>('');
  const [phone, setPhone] = useState<string>('');
  const [email, setEmail] = useState<string>('');
  const [notes, setNotes] = useState<string>('');

  const [isConfirmed, setIsConfirmed] = useState<boolean>(false);
  const [ticketRef, setTicketRef] = useState<string>('');
  const [errorMsg, setErrorMsg] = useState<string>('');

  useEffect(() => {
    if (selectedService) {
      setRitualId(selectedService.id);
    }
    const tomorrow = new Date();
    tomorrow.setDate(tomorrow.getDate() + 1);
    setDate(tomorrow.toISOString().split('T')[0]);
  }, [selectedService]);

  if (!isBookingOpen) return null;

  const currentRitual = siteContent.rituals.find((r) => r.id === ritualId) || siteContent.rituals[0];
  const currentArtisan = siteContent.artisans.find((a) => a.id === artisanId) || siteContent.artisans[0];

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!name.trim() || !phone.trim()) {
      setErrorMsg('Please specify your name and WhatsApp contact number.');
      return;
    }
    setErrorMsg('');
    const refCode = `BK-KOL-${Math.floor(1000 + Math.random() * 9000)}`;
    setTicketRef(refCode);
    setIsConfirmed(true);
  };

  const handleReset = () => {
    setIsConfirmed(false);
    closeBooking();
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/95 backdrop-blur-md overflow-y-auto">
      <div className="relative w-full max-w-xl bg-luxe-card border border-gold-500/50 rounded-sm shadow-2xl overflow-hidden my-auto">
        {/* Header */}
        <div className="p-6 bg-luxe-black border-b border-zinc-800 flex items-center justify-between">
          <div>
            <span className="font-sans text-[11px] uppercase tracking-[0.25em] text-gold-accent font-semibold block">
              Online Booking
            </span>
            <h3 className="font-serif text-2xl font-normal text-white mt-0.5">
              Book an Appointment
            </h3>
          </div>
          <button
            onClick={closeBooking}
            className="p-2 text-zinc-400 hover:text-white rounded-full transition-colors"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Content */}
        <div className="p-6">
          {isConfirmed ? (
            /* Digital Luxury Appointment Ticket */
            <div className="space-y-6 py-4 text-center">
              <div className="w-14 h-14 rounded-full bg-gold-500/10 border-2 border-gold-accent flex items-center justify-center mx-auto text-gold-accent">
                <CheckCircle2 className="w-7 h-7" />
              </div>

              <div>
                <span className="font-sans text-xs text-gold-accent uppercase tracking-widest font-semibold block">
                  Booking Ref: {ticketRef}
                </span>
                <h4 className="font-serif text-2xl font-normal text-white mt-1">
                  Appointment Requested
                </h4>
                <p className="font-serif text-xs text-zinc-400 italic mt-0.5">
                  14/2 Queens Park, Ballygunge Circular Road
                </p>
              </div>

              {/* Ticket Body */}
              <div className="p-5 bg-luxe-black border border-gold-500/30 rounded-xs text-left space-y-3 font-sans text-xs">
                <div className="flex justify-between items-baseline border-b border-zinc-800 pb-2.5">
                  <span className="text-zinc-500 uppercase text-[10px] tracking-wider">Client</span>
                  <span className="text-white font-serif text-sm">{name}</span>
                </div>
                <div className="flex justify-between items-baseline border-b border-zinc-800 pb-2.5">
                  <span className="text-zinc-500 uppercase text-[10px] tracking-wider">Service</span>
                  <span className="text-white text-right max-w-[240px] truncate">{currentRitual.name}</span>
                </div>
                <div className="flex justify-between items-baseline border-b border-zinc-800 pb-2.5">
                  <span className="text-zinc-500 uppercase text-[10px] tracking-wider">Stylist</span>
                  <span className="text-gold-accent font-medium">{currentArtisan.name}</span>
                </div>
                <div className="flex justify-between items-baseline border-b border-zinc-800 pb-2.5">
                  <span className="text-zinc-500 uppercase text-[10px] tracking-wider">Date & Time</span>
                  <span className="text-zinc-300">{date} • {timeSlot}</span>
                </div>
                <div className="flex justify-between items-baseline pt-1">
                  <span className="text-zinc-500 uppercase text-[10px] tracking-wider">Price (INR)</span>
                  <span className="font-serif text-base text-gold-accent font-semibold">{currentRitual.formattedPrice}</span>
                </div>
              </div>

              {/* Demo Notice */}
              <p className="text-[11px] font-sans text-zinc-500">
                {siteContent.demoNotice}
              </p>

              {/* Actions */}
              <div className="flex flex-col sm:flex-row gap-3 pt-2">
                <a
                  href={`https://wa.me/919830122849?text=Hello%20Roop%20Katha,%20I%20have%20booking%20ref%20${ticketRef}%20for%20${encodeURIComponent(
                    currentRitual.name
                  )}`}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="flex-1 py-3 bg-[#25D366] hover:bg-[#20ba5a] text-white text-xs uppercase tracking-wider font-semibold rounded-xs transition-colors flex items-center justify-center gap-2"
                >
                  <WhatsAppIcon className="w-4 h-4 fill-current" />
                  <span>Chat on WhatsApp</span>
                </a>

                <button
                  onClick={handleReset}
                  className="flex-1 py-3 bg-zinc-800 hover:bg-zinc-700 text-zinc-300 text-xs uppercase tracking-wider font-semibold rounded-xs transition-colors"
                >
                  Done
                </button>
              </div>
            </div>
          ) : (
            /* Booking Form */
            <form onSubmit={handleSubmit} className="space-y-4">
              {errorMsg && (
                <div className="p-2.5 bg-rose-500/10 border border-rose-500/30 text-rose-300 text-xs font-sans rounded-xs">
                  {errorMsg}
                </div>
              )}

              {/* Ritual Selector */}
              <div>
                <label className="block text-[10px] font-sans uppercase tracking-widest text-zinc-400 mb-1 font-medium">
                  01. Select Service
                </label>
                <select
                  value={ritualId}
                  onChange={(e) => setRitualId(e.target.value)}
                  className="w-full bg-luxe-black border border-zinc-700 rounded-sm px-3.5 py-2 text-xs text-white focus:outline-none focus:border-gold-accent"
                >
                  {siteContent.rituals.map((r) => (
                    <option key={r.id} value={r.id} className="bg-luxe-dark text-white">
                      {r.name} ({r.formattedPrice} • {r.duration})
                    </option>
                  ))}
                </select>
              </div>

              {/* Artisan Selector */}
              <div>
                <label className="block text-[10px] font-sans uppercase tracking-widest text-zinc-400 mb-1 font-medium">
                  02. Select Stylist
                </label>
                <select
                  value={artisanId}
                  onChange={(e) => setArtisanId(e.target.value)}
                  className="w-full bg-luxe-black border border-zinc-700 rounded-sm px-3.5 py-2 text-xs text-white focus:outline-none focus:border-gold-accent"
                >
                  {siteContent.artisans.map((a) => (
                    <option key={a.id} value={a.id} className="bg-luxe-dark text-white">
                      {a.name} ({a.role})
                    </option>
                  ))}
                </select>
              </div>

              {/* Date & Time */}
              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-[10px] font-sans uppercase tracking-widest text-zinc-400 mb-1 font-medium">
                    03. Date
                  </label>
                  <input
                    type="date"
                    value={date}
                    min={new Date().toISOString().split('T')[0]}
                    onChange={(e) => setDate(e.target.value)}
                    className="w-full bg-luxe-black border border-zinc-700 rounded-sm px-3 py-2 text-xs text-white focus:outline-none focus:border-gold-accent"
                  />
                </div>
                <div>
                  <label className="block text-[10px] font-sans uppercase tracking-widest text-zinc-400 mb-1 font-medium">
                    04. Time Slot
                  </label>
                  <select
                    value={timeSlot}
                    onChange={(e) => setTimeSlot(e.target.value)}
                    className="w-full bg-luxe-black border border-zinc-700 rounded-sm px-3 py-2 text-xs text-white focus:outline-none focus:border-gold-accent"
                  >
                    {siteContent.bookingSlots.map((slot, idx) => (
                      <option key={idx} value={slot} className="bg-luxe-dark text-white">
                        {slot}
                      </option>
                    ))}
                  </select>
                </div>
              </div>

              {/* Guest Details */}
              <div className="grid grid-cols-2 gap-3 pt-2">
                <div>
                  <label className="block text-[10px] font-sans uppercase tracking-widest text-zinc-400 mb-1 font-medium">
                    Guest Name *
                  </label>
                  <input
                    type="text"
                    placeholder="Full Name"
                    value={name}
                    onChange={(e) => setName(e.target.value)}
                    className="w-full bg-luxe-black border border-zinc-700 rounded-sm px-3 py-2 text-xs text-white placeholder-zinc-600 focus:outline-none focus:border-gold-accent"
                  />
                </div>
                <div>
                  <label className="block text-[10px] font-sans uppercase tracking-widest text-zinc-400 mb-1 font-medium">
                    WhatsApp *
                  </label>
                  <input
                    type="tel"
                    placeholder="+91..."
                    value={phone}
                    onChange={(e) => setPhone(e.target.value)}
                    className="w-full bg-luxe-black border border-zinc-700 rounded-sm px-3 py-2 text-xs text-white placeholder-zinc-600 focus:outline-none focus:border-gold-accent"
                  />
                </div>
              </div>

              {/* Price preview */}
              <div className="p-3 bg-luxe-black border border-gold-500/20 rounded-xs flex items-center justify-between text-xs font-sans">
                <span className="text-zinc-400">Estimated Price (INR)</span>
                <span className="font-serif text-base text-gold-accent font-semibold">{currentRitual.formattedPrice}</span>
              </div>

              {/* Submit */}
              <div className="pt-2">
                <button
                  type="submit"
                  className="w-full py-3 bg-gradient-to-r from-gold-600 via-gold-500 to-gold-400 hover:from-gold-500 text-luxe-black font-semibold text-xs uppercase tracking-[0.2em] transition-all duration-200"
                >
                  Confirm Appointment Request
                </button>
              </div>
            </form>
          )}
        </div>
      </div>
    </div>
  );
}
