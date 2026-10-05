/**
 * Domain constants, configurations, and validation/sanitization helpers
 * for Onion Field Assessment.
 */

export const MAX_FILE_SIZE_BYTES = 12 * 1024 * 1024; // 12 MB cap
export const MAX_PHONE_LENGTH = 15;
export const ACCEPTED_IMAGE_MIME_TYPES = [
  'image/jpeg',
  'image/png',
  'image/webp',
  'image/heic',
  'image/jpg',
];

export function formatBytes(bytes) {
  if (!bytes || bytes === 0) return '0 B';
  const k = 1024;
  const sizes = ['B', 'KB', 'MB', 'GB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return `${parseFloat((bytes / Math.pow(k, i)).toFixed(1))} ${sizes[i]}`;
}


/**
 * Clamps numeric input strictly between 0 and 100 in JavaScript.
 * Prevents typed or pasted values exceeding valid percentages.
 * Returns empty string if value is cleared so user can delete/backspace.
 */
export function clampPercent(value) {
  if (value === "" || value === null || value === undefined) {
    return "";
  }
  const cleanStr = String(value).trim();
  if (cleanStr === "") return "";

  const parsed = Number(cleanStr);
  if (Number.isNaN(parsed)) {
    return "";
  }
  if (parsed < 0) return 0;
  if (parsed > 100) return 100;

  return Math.round(parsed * 10) / 10;
}

/**
 * Sanitizes supplier contact number field to only allow digits, spaces, `+`, and `-`.
 * Enforces maximum 15 characters cap.
 */
export function sanitizePhone(value) {
  if (value === null || value === undefined) return "";
  const sanitized = String(value).replace(/[^0-9 + -]/g, "").trimStart();
  return sanitized.slice(0, MAX_PHONE_LENGTH);
}

export const PRODUCING_STATES = [
  "Maharashtra", "Karnataka", "Madhya Pradesh", "Gujarat", "Rajasthan",
  "Bihar", "Andhra Pradesh", "Telangana", "Haryana", "Uttar Pradesh",
  "West Bengal", "Tamil Nadu", "Odisha", "Punjab",
];

export const GRADES = [
  { id: "Grade A", label: "Grade A", badge: "Premium Export" },
  { id: "Grade B", label: "Grade B", badge: "Domestic Standard" },
  { id: "Grade C", label: "Grade C", badge: "Discount / Local" },
  { id: "Reject", label: "Reject / Culled", badge: "Sub-standard" },
];

export const SIZE_CLASSES = [
  { id: "Small", label: "Small (S)", range: "< 35 mm" },
  { id: "Medium", label: "Medium (M)", range: "35-55 mm" },
  { id: "Large", label: "Large (L)", range: "55-70 mm" },
  { id: "Jumbo", label: "Jumbo (XL)", range: "> 70 mm" },
];

export const DEFAULT_VARIETIES = [
  {
    id: "nashik_red",
    name: "Nashik Red",
    type: "Rabi / Storage",
    origin: "Nashik, Maharashtra",
    img: "/varieties/nashik-red.jpg",
    characteristics: "High TSS, firm tight scales, deep purplish-red skin with excellent storage life.",
  },
  {
    id: "bhima_super",
    name: "Bhima Super",
    type: "Kharif / High Yield",
    origin: "ICAR-DOGR, Rajgurunagar",
    img: "/varieties/Bhima-Super-Red-Onion.jpg",
    characteristics: "Vibrant red round bulbs, high yield, moderate pungency.",
  },
  {
    id: "bellary_red",
    name: "Bellary Red",
    type: "Southern High Color",
    origin: "Bellary, Karnataka",
    img: "/varieties/bellary red.jpg",
    characteristics: "Bright coppery red, slightly flattened round bulb, robust export caliber.",
  },
  {
    id: "pune_fursungi",
    name: "Pune Fursungi",
    type: "Export / Rabi",
    origin: "Pune / Ahmednagar, MH",
    img: "/varieties/puna-fursungi-onion.jpg",
    characteristics: "Light copper red, thin neck, tight adherent skin with minimal sprouting.",
  },
  {
    id: "bangalore_rose",
    name: "Bangalore Rose (GI Tag)",
    type: "Southern High Color",
    origin: "Chikkaballapur / Bengaluru, Karnataka",
    img: "/varieties/bangalore-rose-onion.jpg",
    characteristics: "GI Tagged. Spherical flat-topped button bulbs, deep scarlet color, rich in anthocyanin.",
  },
  {
    id: "agrifound_dark_red",
    name: "Agrifound Dark Red",
    type: "Rabi / Storage",
    origin: "NHRDF, Nashik",
    img: "/varieties/agrifound-red-organic-red-onion.jpeg",
    characteristics: "Dark purplish-red globular bulbs, 5–6 cm diameter, firm fleshy scales.",
  },
  {
    id: "pusa_red",
    name: "Pusa Red",
    type: "Rabi / Storage",
    origin: "IARI, New Delhi",
    img: "/varieties/pusa-red-onion.jpg",
    characteristics: "Bronze red, flat-globular, 13–14% TSS, less prone to bolting.",
  },
  {
    id: "white_onion",
    name: "White Onion (Dehydration Grade)",
    type: "Export / Rabi",
    origin: "Bhavnagar / Mahuva, Gujarat",
    img: "/varieties/white-onion.webp",
    characteristics: "Chalky white, high dry matter (18–20% TSS), tailored for dehydration flakes and powder.",
  },
  {
    id: "yellow_granex",
    name: "Yellow Granex",
    type: "Export / Rabi",
    origin: "Subtropical / Winter Crop",
    img: "/varieties/Yellow Granex.jpg",
    characteristics: "Semi-flat golden-yellow scales, sweet juicy flesh, mild pungency.",
  },
  {
    id: "red_creole",
    name: "Red Creole",
    type: "Rabi / Storage",
    origin: "Warm Semi-Arid Tropics",
    img: "/varieties/redcreoleonion.jpg",
    characteristics: "Deep bronze-red skin, flat thick bulbs, heavy pungency, long shelf life.",
  },
  {
    id: "pusa_white_round",
    name: "Pusa White Round",
    type: "Export / Rabi",
    origin: "IARI, New Delhi",
    img: "/varieties/Pusa White Round.jpg",
    characteristics: "Uniform globe shape, pure white wrapper scales, excellent dehydration yield.",
  },
  {
    id: "pusa_madhavi",
    name: "Pusa Madhavi",
    type: "Rabi / Storage",
    origin: "IARI, New Delhi",
    img: "/varieties/Pusa Madhavi.jpg",
    characteristics: "Light reddish-bronze outer skin, mild to medium storage potential.",
  },
  {
    id: "arka_kalyan",
    name: "Arka Kalyan",
    type: "Kharif / High Yield",
    origin: "ICAR-IIHR, Bengaluru",
    img: "/varieties/Arka Kalyan.jpg",
    characteristics: "Pinkish-red globes, resistance to purple blotch disease, thick cured wrapper.",
  },
  {
    id: "agrifound_light_red",
    name: "Agrifound Light Red",
    type: "Rabi / Storage",
    origin: "NHRDF, Nashik",
    img: "/varieties/aflightred.jpg",
    characteristics: "Light copper-red, tight bulb center, high export suitability to Southeast Asia.",
  },
];

export const DEFAULT_DEFECT_SAMPLES = [
  {
    id: "sample_sprout",
    title: "Sprouted Bulb Evidence",
    tag: "[DEFECT: SPROUT (MODERATE)]",
    classTag: "TAG: CLASS II",
    tagBg: "bg-rose-950/85 text-rose-200 border-rose-700",
    badgeBg: "bg-amber-900/85 text-amber-200 border-amber-700",
    img: "/samples/sprouted_sample.jpg",
    description: "Fresh shoot emerging from neck. Moisture exposure during storage.",
  },
  {
    id: "sample_grade_a",
    title: "Pristine Export Grade A",
    tag: "[OK: EXPORT COMPLIANT]",
    classTag: "TAG: GRADE A",
    tagBg: "bg-emerald-950/85 text-emerald-200 border-emerald-700",
    badgeBg: "bg-teal-900/85 text-teal-200 border-teal-700",
    img: "/samples/pristine_sample.jpg",
    description: "Dry intact wrapper scales, cured tight neck, firm solid flesh.",
  },
  {
    id: "sample_doubles",
    title: "Twin / Split Bulb Defect",
    tag: "[DEFECT: DOUBLES (LIGHT)]",
    classTag: "TAG: BORDERLINE",
    tagBg: "bg-amber-950/85 text-amber-200 border-amber-700",
    badgeBg: "bg-stone-900/85 text-stone-200 border-stone-600",
    img: "/samples/twin_sample.jpg",
    description: "Secondary growing point splitting bulb into conjoined twin bulbs.",
  },
];

