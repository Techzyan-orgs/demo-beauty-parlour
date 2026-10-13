'use client';

import React from 'react';
import { siteContent } from '@/data/siteContent';
import { useBooking } from '@/context/BookingContext';
import { MapPin, Phone, Clock, ArrowUpRight } from 'lucide-react';
import WhatsAppIcon from '@/components/WhatsAppIcon';
import FacebookIcon from '@/components/FacebookIcon';
import InstagramIcon from '@/components/InstagramIcon';

export default function SalonFooter() {
  const { openBooking } = useBooking();

  return (
    <footer id="coordinates" className="py-20 bg-luxe-black border-t border-zinc-800 text-zinc-400 relative">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 space-y-16">
        {/* Top Brand Coordinates Row */}
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-12 pb-12 border-b border-zinc-800/80 items-start">
          <div className="lg:col-span-5 space-y-4">
            <div className="flex items-center gap-2">
              <span className="font-serif text-3xl font-normal text-white">
                {siteContent.brand.name}
              </span>
              <span className="font-serif text-xl text-gold-accent italic">
                {siteContent.brand.bengaliName}
              </span>
            </div>

            <p className="font-serif text-sm text-zinc-400 italic max-w-sm">
              “{siteContent.brand.neighborhood} • {siteContent.brand.city}”
            </p>

            <div className="font-sans text-xs tracking-wider text-zinc-500 pt-2">
              GPS: <span className="text-zinc-400 font-medium">{siteContent.brand.coordinates}</span>
            </div>
          </div>

          <div className="lg:col-span-4 space-y-3 font-sans text-xs">
            <span className="text-[11px] uppercase tracking-widest text-gold-accent block font-medium">
              Salon Address & Hours
            </span>
            <div className="flex items-start gap-2 text-zinc-300">
              <MapPin className="w-4 h-4 text-gold-accent shrink-0 mt-0.5" />
              <span className="leading-relaxed">{siteContent.contact.address}</span>
            </div>
            <div className="flex items-center gap-2 text-zinc-400">
              <Clock className="w-4 h-4 text-gold-accent shrink-0" />
              <span>{siteContent.contact.hours}</span>
            </div>
            <div className="flex items-center gap-2 text-zinc-400">
              <Phone className="w-4 h-4 text-gold-accent shrink-0" />
              <span>{siteContent.contact.phone}</span>
            </div>
          </div>

          <div className="lg:col-span-3 space-y-3">
            <span className="font-sans text-[11px] uppercase tracking-widest text-gold-accent block font-medium">
              Bookings & Inquiries
            </span>
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
              onClick={() => openBooking()}
              className="w-full py-3 bg-zinc-900 hover:bg-zinc-800 text-gold-accent border border-gold-500/30 font-sans text-xs uppercase tracking-wider font-medium rounded-xs transition-colors cursor-pointer"
            >
              Book an Appointment
            </button>

            {/* Social Channels with Official Coloured Logos */}
            <div className="pt-2 flex items-center gap-2">
              <a
                href={siteContent.contact.instagramUrl}
                target="_blank"
                rel="noopener noreferrer"
                className="flex-1 flex items-center justify-center gap-2 py-2 px-3 rounded-xs bg-zinc-900 border border-zinc-800 hover:border-pink-500/50 hover:bg-zinc-800/80 transition-all text-xs font-sans text-zinc-300 group"
                title="Follow on Instagram"
              >
                <InstagramIcon className="w-4 h-4 shadow-sm" />
                <span className="group-hover:text-white">Instagram</span>
              </a>

              <a
                href={siteContent.contact.facebookUrl}
                target="_blank"
                rel="noopener noreferrer"
                className="flex-1 flex items-center justify-center gap-2 py-2 px-3 rounded-xs bg-zinc-900 border border-zinc-800 hover:border-blue-500/50 hover:bg-zinc-800/80 transition-all text-xs font-sans text-zinc-300 group"
                title="Follow on Facebook"
              >
                <FacebookIcon className="w-4 h-4 shadow-sm" />
                <span className="group-hover:text-white">Facebook</span>
              </a>
            </div>
          </div>
        </div>

        {/* Bottom Demo Disclaimer & Copyright */}
        <div className="flex flex-col sm:flex-row items-center justify-between gap-4 text-xs font-sans text-zinc-500">
          <div>
            © {new Date().getFullYear()} {siteContent.brand.name}. All rights reserved.
          </div>
          <div className="text-zinc-600 text-center sm:text-right">
            {siteContent.demoNotice}
          </div>
        </div>
      </div>
    </footer>
  );
}
