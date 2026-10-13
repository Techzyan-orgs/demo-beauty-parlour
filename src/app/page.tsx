'use client';

import React from 'react';
import SalonHeader from '@/components/SalonHeader';
import InteractiveApertureHero from '@/components/InteractiveApertureHero';
import SalonSuitesTour from '@/components/SalonSuitesTour';
import SensoryManifesto from '@/components/SensoryManifesto';
import SalonMenuSection from '@/components/SalonMenuSection';
import CustomRitualCalculator from '@/components/CustomRitualCalculator';
import VisualLookbookGrid from '@/components/VisualLookbookGrid';
import TransformationLens from '@/components/TransformationLens';
import ArtisanGuild from '@/components/ArtisanGuild';
import SalonMapSection from '@/components/SalonMapSection';
import SalonFooter from '@/components/SalonFooter';
import BookingModal from '@/components/BookingModal';

export default function HomePage() {
  return (
    <main className="min-h-screen flex flex-col bg-luxe-black text-zinc-100 overflow-x-hidden">
      <SalonHeader />
      <InteractiveApertureHero />
      <SalonSuitesTour />
      <SensoryManifesto />
      <SalonMenuSection />
      <CustomRitualCalculator />
      <VisualLookbookGrid />
      <TransformationLens />
      <ArtisanGuild />
      <SalonMapSection />
      <SalonFooter />
      <BookingModal />
    </main>
  );
}
