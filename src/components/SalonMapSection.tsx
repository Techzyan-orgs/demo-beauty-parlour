'use client';

import React from 'react';
import { siteContent } from '@/data/siteContent';
import { useBooking } from '@/context/BookingContext';
import { MapPin, Navigation, ExternalLink, Clock, Phone } from 'lucide-react';
import WhatsAppIcon from '@/components/WhatsAppIcon';
import FacebookIcon from '@/components/FacebookIcon';
import InstagramIcon from '@/components/InstagramIcon';

export default function SalonMapSection() {
  const { openBooking } = useBooking();

  return (
    <section id="map" className="py-24 lg:py-32 bg-luxe-black text-white relative">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Section Header */}
        <div className="flex flex-col md:flex-row md:items-end justify-between gap-6 mb-12 pb-6 border-b border-zinc-800">
          <div>
            <div className="inline-flex items-center gap-2 text-xs uppercase tracking-[0.25em] text-gold-accent font-sans mb-2">
              <MapPin className="w-3.5 h-3.5" />
              <span>Salon Location & Hours</span>
            </div>
            <h2 className="font-serif text-3xl sm:text-4xl lg:text-5xl font-normal text-white">
              Ballygunge Circular Road
            </h2>
          </div>
          <div className="font-sans text-xs tracking-wider text-zinc-400">
            GPS: <span className="text-gold-accent font-medium">{siteContent.map.coordinates}</span>
          </div>
        </div>

        {/* Map Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-stretch">
          {/* Left: Interactive Embedded Google Map (8 cols) */}
          <div className="lg:col-span-8 rounded-sm overflow-hidden border border-gold-500/30 bg-zinc-950 relative min-h-[420px] shadow-2xl">
            <iframe
              title="Roop Katha Ballygunge Estate Google Map"
              src={siteContent.map.embedUrl}
              className="w-full h-full min-h-[420px] border-0 filter invert-[0.9] hue-rotate-[180deg] contrast-[1.1] grayscale-[0.2]"
              loading="lazy"
              allowFullScreen
            />

            {/* Floating Map Pin Badge */}
            <div className="absolute top-4 left-4 z-10 p-4 rounded-sm bg-luxe-black/95 backdrop-blur-md border border-gold-500/40 max-w-xs shadow-2xl">
              <div className="flex items-center gap-1.5 font-sans text-[11px] uppercase tracking-wider text-gold-accent font-medium">
                <Navigation className="w-3.5 h-3.5" />
                <span>Queens Park Heritage Estate</span>
              </div>
              <p className="font-serif text-base text-white font-normal mt-1">
                {siteContent.brand.name} Luxury Salon
              </p>
              <p className="text-xs text-zinc-300 font-light mt-0.5 leading-relaxed">
                {siteContent.map.address}
              </p>
              <a
                href={siteContent.map.directionsUrl}
                target="_blank"
                rel="noopener noreferrer"
                className="mt-3 inline-flex items-center gap-1.5 text-xs font-sans tracking-wide text-gold-accent hover:text-white transition-colors"
              >
                <span>Navigate in Google Maps</span>
                <ExternalLink className="w-3 h-3" />
              </a>
            </div>
          </div>

          {/* Right: Location Details & Transit Benchmarks (4 cols) */}
          <div className="lg:col-span-4 p-8 rounded-sm bg-luxe-card border border-zinc-800 flex flex-col justify-between space-y-6 shadow-xl">
            <div className="space-y-6">
              <div>
                <span className="font-sans text-[11px] uppercase tracking-widest text-gold-accent font-semibold block mb-1">
                  Estate Address
                </span>
                <p className="font-serif text-lg text-white leading-snug">
                  {siteContent.map.address}
                </p>
                <p className="text-xs text-zinc-400 italic mt-1.5">
                  Landmark: {siteContent.map.landmark}
                </p>
              </div>

              {/* Transit Estimations */}
              <div className="pt-4 border-t border-zinc-800">
                <span className="font-sans text-[11px] uppercase tracking-widest text-zinc-400 block mb-3 font-medium">
                  Proximity & Transit
                </span>
                <div className="space-y-2.5 text-sm font-sans">
                  {siteContent.map.transitTimes.map((item, idx) => (
                    <div key={idx} className="flex justify-between items-center text-zinc-200">
                      <span className="font-light">{item.from}</span>
                      <span className="text-gold-accent font-medium tracking-wide">{item.time}</span>
                    </div>
                  ))}
                </div>
              </div>

              {/* Reception Hours */}
              <div className="pt-4 border-t border-zinc-800 space-y-2 font-sans text-sm">
                <span className="text-[11px] uppercase tracking-widest text-zinc-400 block font-medium">
                  Reception Hours
                </span>
                <div className="flex items-center gap-2 text-zinc-200 font-light">
                  <Clock className="w-4 h-4 text-gold-accent shrink-0" />
                  <span>{siteContent.contact.hours}</span>
                </div>
              </div>
            </div>

            {/* Actions */}
            <div className="pt-4 space-y-2.5">
              <a
                href={siteContent.contact.whatsappLink}
                target="_blank"
                rel="noopener noreferrer"
                className="w-full py-3 bg-[#25D366] hover:bg-[#20ba5a] text-white font-sans text-xs uppercase tracking-wider font-semibold rounded-xs transition-colors flex items-center justify-center gap-2"
              >
                <WhatsAppIcon className="w-4 h-4 fill-current" />
                <span>Chat on WhatsApp</span>
              </a>

              <button
                type="button"
                onClick={() => openBooking()}
                className="w-full py-3 bg-zinc-900 hover:bg-zinc-800 text-gold-accent border border-gold-500/30 font-sans text-xs uppercase tracking-wider font-medium rounded-xs transition-colors cursor-pointer"
              >
                Book an Appointment
              </button>

              {/* Social Channels with Official Coloured Logos */}
              <div className="pt-3 border-t border-zinc-800/80 flex items-center justify-between text-xs">
                <span className="font-sans text-[11px] uppercase tracking-wider text-zinc-400 font-medium">
                  Follow Us:
                </span>
                <div className="flex items-center gap-2">
                  <a
                    href={siteContent.contact.instagramUrl}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="flex items-center gap-1.5 px-3 py-1.5 rounded-xs bg-zinc-900 border border-zinc-800 hover:border-pink-500/50 hover:bg-zinc-800/80 transition-all text-xs font-sans text-zinc-200 group"
                    title="Follow on Instagram"
                  >
                    <InstagramIcon className="w-4 h-4 shadow-sm" />
                    <span className="group-hover:text-white">Instagram</span>
                  </a>

                  <a
                    href={siteContent.contact.facebookUrl}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="flex items-center gap-1.5 px-3 py-1.5 rounded-xs bg-zinc-900 border border-zinc-800 hover:border-blue-500/50 hover:bg-zinc-800/80 transition-all text-xs font-sans text-zinc-200 group"
                    title="Follow on Facebook"
                  >
                    <FacebookIcon className="w-4 h-4 shadow-sm" />
                    <span className="group-hover:text-white">Facebook</span>
                  </a>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
