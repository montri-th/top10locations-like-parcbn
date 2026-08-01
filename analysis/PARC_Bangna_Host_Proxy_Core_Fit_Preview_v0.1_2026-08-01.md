# PARC Bangna Host-Proxy Core-Fit Preview v0.1

**วันที่คำนวณ:** 1 สิงหาคม 2026  
**สถานะ:** Share with caveats — ใช้จัดคิวพิสูจน์ทำเลได้ แต่ยังใช้แทนคะแนน PARC Bangna หรืออนุมัติลงทุนไม่ได้

## คำตอบสั้น

ควรนำ PARC Bangna กลับมาเทียบ แต่ต้องอยู่ในฐานะ **reference นอกกลุ่มผู้สมัคร** ไม่ใช่ผู้สมัครลำดับที่ 746 และไม่ควรนำ locale รอบ PARC อีก 22 รายการกลับมารวมคะแนน

ข้อมูลปัจจุบันยังไม่มี raw inputs ของ venue/catchment PARC ที่หน่วยเดียวกับ locale 745 แห่ง จึงใช้ **ศรีเอี่ยม** เป็น `working host-locale proxy` ชั่วคราว เพราะเป็น primary context ที่มี sampled point ใกล้หมุด PARC ที่สุด 0.30 กม. ตัวเลขนี้เป็นคะแนนบริบท locale ไม่ใช่คะแนนตัวโครงการหรือ measured trade area

## แก้ความเข้าใจเรื่องฐานข้อมูล

| ขั้น | จำนวน | บทบาท |
|---|---:|---|
| Registry ทั้งหมด | 806 | source release v2.3.1 |
| ผ่าน readiness/cosmetic gate | 796 | 626 READY + 170 READY_WITH_COSMETIC_QA_NOTE |
| ตัดข้อมูลที่ไม่มี restaurant evidence ใช้งานได้ | 29 | ไม่ใช้สร้างคะแนน |
| ตัด PARC active context locales | 22 | reference context; ไม่ใช่ผู้สมัคร |
| ฐานสร้าง percentile | 745 | denominator ของ component scores |
| Comparable lane | 574 | ฐานจัดอันดับทำเล PARC-format |
| Challenger lane | 171 | tourist/hotel 169 + office/lunch 2; แยกอ่าน |

ดังนั้นข้อความ `อันดับ /745` ในหน้า v3.4 ไม่ถูกต้อง: **คะแนน percentile เทียบ 745 แต่ลำดับผู้สมัครเทียบ 574**

## Reference ที่ใช้ใน preview

| มิติ | ศรีเอี่ยม host proxy |
|---|---:|
| Resident | 57.70 |
| Routine breadth | 96.12 |
| Accessible routine | 94.75 |
| Activity proof | 92.21 |
| Fresh core opportunity | 74.21 |

Raw inputs สำคัญ: ประชากร 8,213 คน, ความหนาแน่น 4,525.85 คน/ตร.กม., grocery sales area 17,050 ตร.ม., นักเรียน 3,011 คน, office GLA รวม 284,837 ตร.ม. และ restaurant ratings รวม 17,827

Percentile ที่ได้จาก frozen 745: population 71.68, density 46.44, grocery 97.99, students 83.89, hospital beds 0.00, office area 99.19, institution 93.84 และ activity 92.21 ราคาที่ดิน 60,000 บาท/ตร.ว. เป็น diagnostic p71.34 และไม่ได้รับน้ำหนักใน core-fit score

## วิธีคำนวณ

คำนวณ percentile ของ raw inputs เทียบฐาน 745 ที่ตรึงไว้ โดย candidate ใช้ pandas average rank และ reference ที่ไม่อยู่ใน denominator ใช้ frozen out-of-sample ECDF ค่า raw ที่เป็น structural zero ถูกบังคับเป็น p0 เพื่อไม่ให้มวลศูนย์กลายเป็น percentile กลางปลอม

\[
R=\sqrt{P_{population}\times P_{density}}
\]

\[
Institution=.65\times strongest+.35\times second\ strongest
\]

โดย strongest/second strongest มาจาก student, hospital-bed และ office-area percentiles

\[
B=.55P_{grocery\ area}+.45Institution
\]

\[
A=P_{restaurant\ ratings}
\]

เพื่อเชื่อมกับมุม Routine ใน analytical release เดิม แสดง Accessible routine เพิ่มเติมด้วยสูตร

\[
AR=.65B+.35A
\]

แต่ Fresh opportunity ใช้ \(B\) โดยตรง ไม่ใช้ \(AR\)

คะแนนความคล้ายบริบท:

\[
Similarity=100-[.55|R-R_p|+.25|B-B_p|+.20|A-A_p|]
\]

คะแนนความแข็งแรงของโอกาส core:

\[
Opportunity=.55R+.25B+.20A
\]

เมื่อจำเป็นต้องมีลำดับเดียว ใช้ harmonic mean 50/50 เป็น decision score และทดสอบ sensitivity โดยให้น้ำหนัก Similarity 40%, 50% และ 60% แยกกัน

## Top 10 core-fit ก่อน route, site และ economics gates

| อันดับ | Locale | Similarity | Opportunity | Decision | ช่วงอันดับ 40/50/60 | Land pctl. | อ่านอย่างไร |
|---:|---|---:|---:|---:|---:|---:|---|
| 1 | เอกมัย-ใต้ | 94.23 | 79.57 | 86.28 | 1–4 | 91.18 | central leader แต่ land pressure สูง |
| 2 | วังหิน-ใต้ | 80.88 | 90.70 | 85.51 | 1–7 | 53.77 | opportunity-led และ land diagnostic ปานกลาง |
| 3 | สัมมากร | 98.57 | 75.16 | 85.28 | 2–11 | 46.59 | profile ใกล้ proxy ที่สุด แต่ไวต่อน้ำหนัก |
| 4 | พระราม 3-ตะวันออก | 87.60 | 82.93 | 85.20 | 4–6 | 88.48 | อันดับนิ่ง แต่ economics เป็นด่านหลัก |
| 5 | บางรัก | 90.93 | 79.93 | 85.08 | 3–7 | 96.16 | fit สูง แต่ land pressure สูงมาก |
| 6 | คลองจั่น | 88.70 | 80.69 | 84.50 | 6–8 | — | fit/โอกาสสมดุล แต่ land evidence ขาด |
| 7 | เจริญราษฎร์ | 80.53 | 88.68 | 84.41 | 2–9 | 82.57 | opportunity สูงแต่ sensitivity และ land pressure สูง |
| 8 | อารีย์ | 90.34 | 78.98 | 84.28 | 5–10 | 84.50 | fit สูง; site economics เป็นด่านหลัก |
| 9 | เย็นอากาศ | 87.00 | 80.94 | 83.86 | 8–9 | 85.92 | ลำดับนิ่งแต่ land pressure สูง |
| 10 | สำเหร่ | 76.75 | 91.21 | 83.36 | 5–16 | 67.21 | opportunity สูงมาก แต่ความคล้ายและอันดับไวต่อน้ำหนัก |

## คิวที่ควรนำไปพิสูจน์ต่อ

1. **เอกมัย-ใต้** — central leader และ profile fit สูง ใช้ทดสอบว่าความคล้ายยังคุ้มหลัง land/economics หรือไม่
2. **วังหิน-ใต้** — opportunity สูงสุดในกลุ่มนำและ land diagnostic ปานกลาง ใช้ทดสอบ route/supply
3. **สัมมากร** — profile ใกล้ proxy ที่สุดและ land diagnostic ต่ำกว่ากลุ่ม fit สูงอื่นอย่างชัดเจน
4. **พระราม 3-ตะวันออก** — อันดับนิ่ง #4–6 แต่ land pressure สูง จึงต้องเปิด economics gate เร็ว

นี่คือคิว `route + site + competition + economics validation` ที่ตั้งใจให้หลากหลาย ไม่ใช่ score band หรือคำแนะนำซื้อที่ดิน ตลาดพลู-ใต้และราชเทวีอยู่ใน sensitivity union แม้ไม่อยู่ central Top 10 ส่วนคลองจั่นต้องปิดช่องว่าง land evidence ก่อนผ่าน economics gate

## Validation report

### Overall assessment: Share with caveats

### ตรวจผ่าน

- Registry locale IDs ไม่ซ้ำและ join ระหว่าง Index/Facts/Benchmarks ครบ 806 รายการ
- Filter สร้าง 745 ได้ตรงกับ analytical brief
- Comparable lane ได้ 574 และ challenger lane ได้ 171 ตรงกัน
- PARC context IDs 22 รายการไม่อยู่ในผู้สมัคร
- สูตร Resident, Routine breadth, Activity และ Accessible routine ที่กู้คืนได้ตรวจย้อนกลับกับ 16 แถวที่เผยแพร่แล้วตรงทั้งหมดหลังปัดตามหน้าจอ; สิบแถวพอร์ตที่แสดงสองตำแหน่งคลาดสูงสุด 0.005 จุด
- Top 10 preview มีข้อมูล R/B/A ครบและ score อยู่ในช่วง 0–100
- Sensitivity ใช้สามน้ำหนักที่ประกาศล่วงหน้าและ tie-break ด้วย locale ID
- Operating receipts, tenant performance และ customer behavior ของ PARC ไม่ถูกนำมาเป็น candidate features

### Blockers ต่อ exact PARC benchmark

1. Working catchment PARC 26.3154 ตร.กม. คนละ observation unit กับ locale proxy ศรีเอี่ยม 1.814687 ตร.กม.
2. PARC Locale Insight ยังไม่มี approved percentile capsule, catchment population หรือ raw routine inputs ที่ aggregate ด้วยกติกาเดียวกับ 745
3. Original v3.3 full analytical generator, competition/barrier artifacts และ frozen 574-row output ไม่อยู่ใน repo/Drive/GitHub ที่ค้นได้ แม้สูตร Fresh components จะกู้คืนและตรวจสอบได้แล้ว
4. Preview นี้ยังไม่มี barrier-aware access, competition pressure, parcel, frontage, parking, servicing และ project economics

### ผลต่อการใช้งาน

- ใช้ preview นี้เพื่อหา **ทำเลที่ควรไปพิสูจน์ต่อ** ได้
- ห้ามเรียก 57.70/96.12/92.21 ว่า “คะแนน PARC Bangna” โดยไม่ใส่คำว่า `ศรีเอี่ยม host-locale proxy`
- Fresh components ใช้สูตรเดียวกับ v3.3 ที่กู้คืนได้ แต่ห้ามนำ preview ไปแทน Balanced/market/stability score เพราะยังไม่มี barrier และ competition components ของ proxy
- Exact PARC benchmark ต้อง regenerate PARC และผู้สมัครด้วย geometry/catchment rule เดียวกัน หรืออย่างน้อยยืนยัน home-locale polygon ที่ครอบหมุด PARC ก่อน

## แหล่งอ้างอิง

- [Venue Locale Registry v2.3.1](https://docs.google.com/spreadsheets/d/1ICFCff5IsjBfkgjej42_MdWuNfYaGsklKMuxpQtB9jQ)
- `PARC_Bangna_Project_Locale_Pack_v1_1_2026-07-22.md`
- `ijji_locale_insight_parc_bangna_v2_3.md`
- `parc_bangna_active_locale_refs_v0_1.json`
- `parc_bangna_locale_crosswalk_v0_1.json`
- `analysis/PARC_Bangna_Fresh_Locale_Screen_Analysis_and_UXUI_Brief_v0.1_2026-07-28.md`
- `analysis/PARC_Bangna_Fresh_Locale_Screen_Multi_Lens_Board_Brief_v0.4_2026-07-28.md`

Machine-readable result: `analysis/parc-host-proxy-core-fit-preview-v0.1.json`
