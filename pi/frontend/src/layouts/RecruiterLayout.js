import React from 'react';

export default function RecruiterLayout({ children }) {
  return (
    <div>
      <header>Recruiter</header>
      <main>{children}</main>
    </div>
  );
}
