// Service menu groups (PLAN-004, approved by Rob 22/11/2026).
// Used by the header, footer and homepage so the grouping lives in one place.

export interface MenuLink {
  name: string;
  href: string;
  children?: MenuLink[];
}

export interface MenuGroup {
  heading: string;
  links: MenuLink[];
}

export const serviceMenu: MenuGroup[] = [
  {
    heading: 'Sheet Metal',
    links: [
      { name: 'Laser Profiling', href: '/laser-profiling/' },
      { name: 'Folding & Pressing', href: '/folding-pressing/' },
      { name: 'Fabrication & Welding', href: '/fabrication-and-welding/' },
    ],
  },
  {
    heading: 'Machining',
    links: [
      {
        name: 'CNC Machining',
        href: '/cnc-machining/',
        children: [
          { name: 'Milling', href: '/milling/' },
          { name: 'Turning', href: '/turning/' },
        ],
      },
    ],
  },
  {
    heading: 'Design',
    links: [{ name: 'CAD Design', href: '/cad/' }],
  },
];

/** Every service link, flattened (parents before their children). */
export const allServiceLinks: MenuLink[] = serviceMenu.flatMap((g) =>
  g.links.flatMap((l) => [l, ...(l.children ?? [])])
);
