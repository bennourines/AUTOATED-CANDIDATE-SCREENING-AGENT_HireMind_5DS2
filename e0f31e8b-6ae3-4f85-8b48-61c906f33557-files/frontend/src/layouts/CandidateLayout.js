import React from 'react';

export default function CandidateLayout({ children }) {
  return (
    <div>
      <header>Candidate</header>
      <main>{children}</main>
    </div>
  );
}
