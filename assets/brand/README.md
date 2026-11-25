# HiddenCare Brand and Favicon Set

## Chosen Direction: Direction 1 (Serif Monogram)

Direction 1 was chosen for its quiet editorial authority and direct conceptual fit with HiddenCare. Two hand drawn transitional serif stems frame a broken hairline crossbar, where a single emerald point bridges the gap to represent the patient missed by clinical records and revealed by a laboratory value. Unlike the roundel and ruled notebook studies, the serif monogram retains a distinct, solid silhouette at 16 pixels while feeling native to an academic poster or university press monograph. Its proportions align naturally with the editorial serif typography of the HiddenCare web interface.

## Grid and Proportions

* Primary canvas: 64 by 64 units (`viewBox="0 0 64 64"`).
* Outer bounding box: x from 9.0 to 55.0 (46.0 units wide), y from 10.0 to 54.0 (44.0 units tall), leaving balanced optical margins inside the square.
* Stems: centered at x = 17.5 and x = 46.5, width 6.8 units, with 1.8 unit serif slabs and 5.0 unit cubic Bezier brackets (control ratio 0.34).
* Broken crossbar: height 1.9 units, optically raised to y = 31.4 (0.6 units above geometric center), with a 12.4 unit central opening (x = 25.8 to x = 38.2).
* Accent point: circle centered at (32.0, 31.4) with radius 3.15 units, preserving 3.05 units of open space on each side before the crossbar terminals.
* Micro scale variant (`favicon.svg`): stems thickened to 10.0 units, serif slabs to 4.0 units, crossbar to 4.2 units, and dot radius to 4.6 units for 16 pixel clarity.

## Colour Palette and Contrast Ratios

| Role | Hex Code | Contrast on `#ffffff` | Contrast on `#f8fafc` | Contrast on `#0b1220` |
| :--- | :--- | :---: | :---: | :---: |
| Deep Teal (Primary, light ground) | `#0f5d57` | 7.71 : 1 | 7.37 : 1 | 2.43 : 1 |
| Emerald (Accent, light ground) | `#059669` | 3.77 : 1 | 3.60 : 1 | 4.97 : 1 |
| Pale Teal (Primary, dark ground) | `#d8ece9` | 1.24 : 1 | 1.19 : 1 | 15.13 : 1 |
| Bright Emerald (Accent, dark ground) | `#34d399` | 1.92 : 1 | 1.84 : 1 | 9.74 : 1 |
| Ink Slate (Monochrome print) | `#0f172a` | 17.85 : 1 | 17.06 : 1 | 1.05 : 1 |
| Calm Paper Surface | `#f8fafc` | 1.05 : 1 | 1.00 : 1 | 17.89 : 1 |

Because Deep Teal `#0f5d57` reaches 7.71 : 1 on white but 2.43 : 1 on dark navy `#0b1220`, a dedicated dark variant (`hiddencare-mark-dark.svg`) and a dark scheme media rule inside `favicon.svg` are provided so contrast exceeds 3 : 1 on both light and dark surfaces.

## Typography

The lockup (`hiddencare-lockup.svg`) sets HiddenCare in Noto Serif Display SemiBold and Algorithmic Epidemiology Lab in tracked Noto Serif Medium (both released under the SIL Open Font License), converted entirely to vector paths so no external font file is required.

## File Inventory

| File | Size |
| :--- | ---: |
| `hiddencare-mark.svg` | 1,175 bytes |
| `hiddencare-mark-dark.svg` | 1,175 bytes |
| `hiddencare-mark-mono.svg` | 1,200 bytes |
| `favicon.svg` | 1,323 bytes |
| `favicon.ico` | 3,006 bytes |
| `favicon-96x96.png` | 2,343 bytes |
| `apple-touch-icon.png` | 2,934 bytes |
| `icon-192.png` | 4,787 bytes |
| `icon-512.png` | 11,721 bytes |
| `icon-maskable-512.png` | 7,879 bytes |
| `site.webmanifest` | 606 bytes |
| `hiddencare-lockup.svg` | 16,381 bytes |
| `social-share.png` | 45,048 bytes |
| `concepts.png` | 107,463 bytes |
| `refinement_log.md` | 2,418 bytes |

## HTML Tags for `<head>`

```html
<link rel="icon" type="image/svg+xml" href="/assets/brand/favicon.svg">
<link rel="icon" type="image/png" sizes="96x96" href="/assets/brand/favicon-96x96.png">
<link rel="shortcut icon" href="/assets/brand/favicon.ico">
<link rel="apple-touch-icon" sizes="180x180" href="/assets/brand/apple-touch-icon.png">
<link rel="manifest" href="/assets/brand/site.webmanifest">
<meta name="theme-color" content="#f8fafc" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#0b1220" media="(prefers-color-scheme: dark)">
```
