# PARC Bangna — Fresh Locale Screen
## Competition-aware Board Brief และ UX/UI Specification

**ฉบับ:** v0.2 — Board decision checkpoint  
**วันที่:** 28 กรกฎาคม 2026  
**สถานะ:** พร้อมใช้ขออนุมัติศึกษารายละเอียด Top 10; ยังไม่ใช่คำตัดสินเลือกแปลง ลงทุน หรือซื้อที่ดิน  
**พื้นที่ศึกษา:** กรุงเทพมหานคร  
**ฐานอ้างอิง:** Fresh Locale Screen v0.1, Venue Locale Insight v2.3.1, Venue Locale Fundamental v0.2.0-rc1 และหลักฐานผู้ประกอบการที่ตรวจ ณ 28 กรกฎาคม 2026

---

## 1. คำตอบสำหรับ CEO, CFO และ Board

### ข้อเสนอเพื่ออนุมัติ

> **อนุมัติให้ศึกษารายละเอียด Top 10 ทำเลที่นำเสนอครบทั้ง 10 แห่ง**  
> โดยใช้คู่แข่งเป็น kill test, ใช้เวลาเดินทางจริงแทนวงกลม และบังคับให้ทำเลที่ทับกันแข่งกันเองก่อนเสนอ shortlist รอบลงทุน

การอนุมัติครั้งนี้ **ไม่ใช่**:

- การอนุมัติให้ศึกษาทั้ง 745 locales แบบลงรายละเอียดเท่ากัน
- การอนุมัติเลือกผู้ชนะ
- การอนุมัติหาแปลง ซื้อที่ดิน หรืออนุมัติ CAPEX
- การรับรองว่าคะแนน Fresh เดิมรวมผลคู่แข่งครบแล้ว

### เหตุผลที่ควรอนุมัติ

1. Fresh Screen เริ่มจากทั้งจักรวาลและได้ 10 สัญญาณตลาดที่มีฐานคน กิจวัตร และการใช้ชีวิตนอกบ้านแข็งแรง
2. การตรวจคู่แข่งรอบนี้พบว่า **ไม่มีทำเลใดเป็น low-competition whitespace**
3. คู่แข่งจำนวนมากทำ “green / family / wellness / food / community” อยู่แล้ว จึงห้ามใช้คำว่า “สวน สงบ เป็นธรรมชาติ” เป็นจุดต่างเพียงลำพัง
4. Top 10 มีตลาดที่น่าจะทับกันอย่างน้อย 3 กลุ่ม การลงรายละเอียดพร้อมกันทำให้ Board เลือก “ตลาดจริง” แทนการเลือกหลายชื่อที่ใช้ลูกค้าก้อนเดียวกัน
5. การศึกษารอบถัดไปสามารถวาง kill criteria ล่วงหน้า ทำให้หยุดทำเลที่ไม่มี route advantage, ไม่มี unmet job หรือไม่มีแปลงที่เข้า–ออกได้ ก่อนใช้เงินมาก

### ข้อค้นพบสำคัญที่สุด

**คู่แข่งไม่ควรถูกใช้เป็นตัวหักคะแนนแบบนับจำนวนดิบ**  
ศูนย์จำนวนมากอาจแปลว่าตลาดแข็งแรง แต่ทำเลจะน่าสนใจต่อเมื่อเราพิสูจน์ได้ว่า:

- ลูกค้าเข้าถึงเราได้ง่ายกว่าในกิจวัตรจริง
- คู่แข่งเดิมยังทำบาง job ได้ไม่ดี
- PARC สามารถชนะด้วยรูปแบบที่เฉพาะกว่า ไม่ใช่เพียงบรรยากาศคล้ายกัน
- แปลงมี access, visibility, parking และ economics ที่รองรับข้อเสนอจริง

---

## 2. สิ่งที่วิเคราะห์ใหม่ในรอบนี้

### 2.1 งานที่ทำแล้ว

- ยึด Fresh Screen v0.1 เป็น baseline เดียว: 806 records → 745 locales ที่ให้คะแนนได้ → 574 primary lane + 171 challenger lane
- รักษาคะแนน Fresh เดิมไว้ ไม่ปะปนกับคะแนน Release 1.5/1.6
- ตรวจฐาน Venue Locale Fundamental v0.2.0-rc1 จำนวน 10,873 records เพื่อค้นหาคู่แข่งรอบ Top 10
- ตรวจสถานะและข้อมูลขนาดจากแหล่งผู้ประกอบการ/เจ้าของสินทรัพย์สำหรับศูนย์ที่มีผลสูง
- จัดกลุ่มคู่แข่งที่อยู่ในโครงการเดียวกันเพื่อไม่ให้นับซ้ำ เช่น ICONSIAM + ICS
- แยก `competition pressure` ออกจาก `strategic gap`
- เพิ่ม competition pressure band, จุดต่างที่ต้องพิสูจน์ และ kill test รายทำเล
- กำหนด map contract ใหม่: candidate reference point, simplified metric basemap, competitor marker, marker detail และ fallback list
- เปลี่ยน CTA จาก “อนุมัติทำ 745” เป็น “อนุมัติศึกษารายละเอียด Top 10”

### 2.2 สิ่งที่ยังห้ามเรียกว่าทำเสร็จ

ยังไม่สามารถประกาศ “Top 10 ขั้นตัดสินจากทั้ง 745 locales หลังรวมคู่แข่ง” ได้อย่างซื่อสัตย์ เพราะยังขาด:

- competitor census ที่ใช้ขอบเขตและกติกาเดียวกันครบทั้ง 745 locales
- route matrix ที่ผ่านสะพาน ท่าเรือ ทางด่วน คลอง รถไฟ และทางกลับรถจริง
- competitor GLA / Retail NLA ที่ยืนยันได้ในสัดส่วนเท่ากันทุกพื้นที่
- parent-cluster deduplication ครบทั้งฐาน
- locale polygons ที่ส่งมอบในรูป GeoJSON/WKT พร้อม lineage
- market-overlap consolidation บน network catchment

ดังนั้นฉบับนี้ใช้คำว่า:

- **Fresh baseline rank** สำหรับอันดับเดิม
- **competition pressure band** สำหรับความกดดันที่ตรวจได้
- **study sequence** สำหรับลำดับทำงาน ไม่ใช่อันดับลงทุน

ไม่สร้างคะแนนทศนิยมใหม่ที่ดูแม่นเกินหลักฐาน

---

## 3. ผล competition-aware screen

### 3.1 ภาพรวม

| Fresh rank | Locale | Fresh score | Competition pressure | สิ่งที่เปลี่ยนหลังตรวจคู่แข่ง | Study stance |
|---:|---|---:|---|---|---|
| 1 | ตลาดพลู-ใต้ | 93.8 | สูง | The Mall Lifestore Tha Phra อยู่ใกล้มาก; generic family mall ไม่ใช่ช่องว่าง | พิสูจน์ก่อน: quick routine + open-air regular refuge |
| 2 | สำเหร่ | 91.2 | สูง / route-sensitive | Riverside Plaza อยู่แทบชิดจุดอ้างอิง และ The Mall Tha Phra อยู่ใกล้ | แข่งกับตลาดพลูเพื่อเป็นตัวแทนกลุ่ม |
| 3 | วังหิน-ใต้ | 90.7 | สูงมาก | EastVille, Crystal, CDC ครอบคลุม nature, pet, wellness, food แล้ว | hurdle สูงสุดด้าน concept differentiation |
| 4 | เจริญราษฎร์ | 88.7 | สูงมาก | KINGSQUARE, Terminal 21 และ Central Rama 3 อยู่ในสนามเดียวกัน | เทียบกับพระราม 3 บน route จริง |
| 5 | บางซ่อน | 86.7 | สูง | Gateway at Bangsue และ Lotus’s Prachachuen เป็น direct routine supply | แข่งกับบางโพเพื่อเหลือตัวแทนเดียว |
| 6 | วงเวียนใหญ่-ตะวันออก | 86.1 | สูง | Platform อยู่ใกล้มาก; ICONSIAM/ICS/SENA Fest เพิ่มแรงดึงดูด | เดินหน้าต่อเมื่อแปลง/ทางเข้าเหนือกว่า |
| 7 | บางขุนนนท์-ใต้ | 84.7 | สูงมากระดับภูมิภาค | Central Pinklao แข็งแรงระดับภูมิภาค แต่ยังมีสมมติฐานเรื่อง neighbourhood friction | มี relative room เฉพาะ daily job แต่ต้องพิสูจน์ access |
| 8 | แยกบ้านแขก | 84.0 | กลาง–สูง / route-sensitive | Platform และกลุ่มริมน้ำอยู่ใกล้; Old Siam เป็น niche benchmark ข้ามฝั่ง | ความเสี่ยงสูงจากทั้ง overlap และอันดับแกว่ง |
| 9 | บางโพ-ตะวันออก | 83.1 | สูง | จุดอ้างอิงอยู่ใกล้ Gateway at Bangsue มาก | ต้องพิสูจน์ว่าไม่ใช่ตลาดเดียวกับบางซ่อน |
| 10 | พระราม 3-ตะวันออก | 82.9 | สูงมาก | Central Rama 3 + Bangkok Square + KINGSQUARE; T21 เป็น route-dependent | น่าสนใจเฉพาะข้อเสนอ low-rise / quick routine ที่คมมาก |

### 3.2 ความหมายของ pressure band

`สูงมาก` ในรอบนี้หมายถึงอย่างน้อยหนึ่งข้อ:

- มีคู่แข่งผลกระทบสูงในบริบทระยะตรงประมาณ 1 กม. หรือน้อยกว่า; หรือ
- มีคู่แข่งผลกระทบสูง/กลางสูงอย่างน้อย 3 แห่งในบริบทประมาณ 3 กม. หลังลดการนับซ้ำเบื้องต้น

`สูง` หมายถึง:

- มีคู่แข่งผลกระทบสูงอย่างน้อยหนึ่งแห่งในบริบทประมาณ 3 กม.; หรือ
- มี supply ระดับภูมิภาคใกล้เคียง แต่ผลจริงยังขึ้นกับเส้นทางและสิ่งกีดขวาง

`กลาง–สูง / route-sensitive` หมายถึงมีรายชื่อและจุดดึงดูดที่น่าจะมีผล แต่การข้ามแม่น้ำ โครงข่ายถนน หรือ fragmented street retail ยังทำให้ direct pressure สรุปไม่ได้จากระยะตรง

ระยะดังกล่าวใช้เพื่อ **จัดคิวตรวจและวาดแผนที่เท่านั้น** ไม่ใช่ catchment และไม่ถูกนำมาหักคะแนน Fresh

---

## 4. ลำดับการศึกษาที่แนะนำ

Board อนุมัติครบ 10 แห่ง แต่ทีมไม่ควรทำทุกแห่งด้วยคำถามเดียวกัน

### Wave A — prove or kill ก่อน

1. **ตลาดพลู-ใต้** — baseline แข็งแรงที่สุด แต่ต้องตอบให้ได้ว่าจะชนะ The Mall Tha Phra ด้วย job ใด
2. **บางขุนนนท์-ใต้** — ทดสอบว่ามี neighbourhood access gap ที่ Central Pinklao ไม่ตอบหรือไม่
3. **พระราม 3-ตะวันออก** — ทดสอบ quick routine / low-rise refuge ท่ามกลาง regional supply
4. **วังหิน-ใต้** — concept collision สูงที่สุด; ผ่านต่อได้เมื่อมี unmet job ที่ EastVille/Crystal/CDC ไม่ครอง

### Wave B — เลือกตัวแทนจากตลาดที่ทับกัน

5. **เจริญราษฎร์** เทียบ **พระราม 3-ตะวันออก**
6. **บางซ่อน** เทียบ **บางโพ-ตะวันออก**
7. **สำเหร่**, **วงเวียนใหญ่-ตะวันออก**, **แยกบ้านแขก** เทียบกับ **ตลาดพลู-ใต้**

ลำดับนี้เป็น **work sequence** ไม่ใช่ investment ranking

---

## 5. วิเคราะห์รายทำเล

### 5.1 ตลาดพลู-ใต้

**Fresh signal:** อันดับ 1, คะแนน 93.8, ช่วงอันดับ 1–1  
**Pressure:** สูง

**คู่แข่งหลัก**

- The Mall Lifestore Tha Phra — บริบทระยะตรงประมาณ 0.51 กม.; สถานะเปิดยืนยันจากผู้ประกอบการ; current GLA ยังไม่ยืนยัน
- Riverside Plaza Bangkok — ประมาณ 1.99 กม.; lifestyle/community supply; current GLA ยังไม่ยืนยัน
- Platform Wongwian Yai — ประมาณ 2.16 กม.; ขนาดยังไม่ยืนยัน
- ICONSIAM — ประมาณ 3.74 กม.; เป็น destination cluster และต้องผ่าน route/crossing ก่อนนับผล

**คู่แข่งทำได้ดีอยู่แล้ว**

The Mall Tha Phra มี grocery, food, fashion, beauty, sports, electronics, kids และ entertainment ครบ จึงไม่ควรเสนอ PARC เป็น “ศูนย์ครอบครัวที่มีอาหารและสวน” แบบกว้าง

**สิ่งที่ต้องเป็นจริงจึงควรไปต่อ**

- ถึงง่ายกว่าในกิจวัตร 10–15 นาทีของคนพื้นที่
- ใช้เวลาสั้นกว่า สงบกว่า และตัดสินใจง่ายกว่า regional mall
- โปรแกรม open-air / pet / wellness ไม่ใช่เพียง decoration แต่ลด friction ของการมาใช้ซ้ำ

**Kill test**

หยุดหากไม่มี route advantage, ไม่มีแปลงเข้า–ออกง่าย หรือผู้ใช้ไม่เห็น job ที่ต่างจาก The Mall

### 5.2 สำเหร่

**Fresh signal:** อันดับ 2, คะแนน 91.2, ช่วงอันดับ 2–3  
**Pressure:** สูง / route-sensitive

**คู่แข่งหลัก**

- Riverside Plaza Bangkok — จุดอ้างอิงอยู่ใกล้มาก; ต้องตรวจว่า locale center ไม่ได้ถูก venue เดิมครอบอยู่แล้ว
- The Mall Lifestore Tha Phra — ประมาณ 1.49 กม.
- SENA Fest — ประมาณ 2.37 กม.; rental/leasable area 8,931 ตร.ม. ณ สิ้นปี 2025 ตาม One Report (นิยามไม่ควรถูกเทียบกับ Retail NLA โดยตรง); หน้าโครงการเดิมระบุ commercial space 9,811 ตร.ม.
- Platform Wongwian Yai — ประมาณ 2.44 กม.
- Terminal 21 Rama 3 — ประมาณ 2.40 กม. ระยะตรง แต่ข้ามแม่น้ำ; ห้ามนับเป็น direct pressure ก่อนทำ route matrix

**สิ่งที่ต้องเป็นจริง**

สำเหร่ต้องมี micro-catchment และทางเข้า–ออกที่ต่างจากตลาดพลูอย่างมีนัยสำคัญ ไม่ใช่เพียง locale name คนละชื่อ

**Kill test**

หาก network overlap กับตลาดพลูเกินเกณฑ์หรือ Riverside Plaza ครองกิจวัตรเดียวกัน ให้เก็บสำเหร่เป็น backup ไม่เดินหน้าคู่กัน

### 5.3 วังหิน-ใต้

**Fresh signal:** อันดับ 3, คะแนน 90.7, ช่วงอันดับ 2–3  
**Pressure:** สูงมาก และเป็น concept-collision hurdle สูงสุด

**คู่แข่งหลัก**

- Central EastVille — ประมาณ 1.94 กม.; Retail NLA 35,732 ตร.ม.; nature/outdoor, pet park, rooftop jogging, food hall, wellness และ fitness
- The Crystal Ekamai-Ramindra — ประมาณ 2.44 กม.; Retail NLA 30,823 ตร.ม.; occupancy 96.9% ณ 1Q26
- CDC — ประมาณ 2.38 กม.; Retail NLA 35,957 ตร.ม.; design/home, fitness, food และ grocery
- Imperial World Ladprao — ประมาณ 2.79 กม.; เปิดให้บริการ แต่ current size ยังไม่ยืนยัน
- The Walk Kaset-Nawamin — ประมาณ 4.27 กม.; home/lifestyle cluster; ขนาดทั้งศูนย์ยังไม่ยืนยัน

**คู่แข่งทำได้ดีอยู่แล้ว**

EastVille และ Crystal ครองความหมาย nature, pet, wellness, family และ quality time อยู่แล้ว ขณะที่ CDC ครอง home/design destination

**สิ่งที่ต้องเป็นจริง**

PARC ต้องชนะด้วย micro-location, daily convenience, recognition และ 60–90 minute regular refuge—not “green lifestyle” แบบเดียวกับตลาด

**Kill test**

หยุดหาก customer research ไม่พบ unmet job ที่ชัด หรือ route 10–15 นาทีถูก regional cluster ครอบเกือบทั้งหมด

### 5.4 เจริญราษฎร์

**Fresh signal:** อันดับ 4, คะแนน 88.7, ช่วงอันดับ 4–5  
**Pressure:** สูงมาก

**คู่แข่งหลัก**

- KINGSQUARE Community Mall — ประมาณ 1.23 กม.; direct family/routine overlap
- Terminal 21 Rama 3 — ประมาณ 1.48 กม.; 7 retail floors; current GLA ยังไม่ยืนยัน
- Central Rama 3 — ประมาณ 2.27 กม.; Retail NLA 48,328 ตร.ม.
- SENA Fest — ประมาณ 2.73 กม.; partial lifestyle overlap
- Asiatique — destination/experience supply; ต้องใช้เส้นทางจริงและไม่ตีความเป็น everyday substitute โดยอัตโนมัติ

**สิ่งที่ต้องเป็นจริง**

ทำเลต้องสร้าง daily catchment ฝั่งเดียวกันที่ไม่ถูก KINGSQUARE/T21/Central กินหมด และต้องต่างจากพระราม 3-ตะวันออกพอที่จะเป็นคนละตลาด

**Kill test**

หาก Charoen Rat และ Rama 3 ใช้ demand cells ชุดเดียวกัน ให้เลือกตัวแทนจาก access + parcel economics ไม่เดินหน้าทั้งคู่

### 5.5 บางซ่อน

**Fresh signal:** อันดับ 5, คะแนน 86.7, อยู่ Top 10 ทุกกรณี sensitivity เดิม  
**Pressure:** สูง

**คู่แข่งหลัก**

- Gateway at Bangsue — ประมาณ 0.94 กม.; family/community offer, dining, health/beauty, education, cinema, fitness, kids และ sky garden; total area >95,000 ตร.ม. แต่ owner ไม่ได้ยืนยันเป็น GLA
- Lotus’s Prachachuen — ประมาณ 0.96 กม.; current branch verified; size unknown
- Central Ladprao — ประมาณ 3.47 กม.; Retail NLA 43,410 ตร.ม.; route-dependent
- Union Mall — ประมาณ 3.52 กม.; fashion/youth destination; size unknown
- The Central Phaholyothin — pipeline Q1 2027, NLA ประมาณ 100,000 ตร.ม.; scenario risk ไม่ใช่ operating supply ปัจจุบัน

**สิ่งที่ต้องเป็นจริง**

ช่องว่างต้องเป็น low-friction neighbourhood routine ที่ถูกถนน/ทางรถไฟ/จุดข้ามป้องกันจาก Gateway—not generic family community mall

**Kill test**

หาก catchment ทับ Gateway และบางโพ-ตะวันออกสูง ให้เลือกตัวแทนเดียว

### 5.6 วงเวียนใหญ่-ตะวันออก

**Fresh signal:** อันดับ 6, คะแนน 86.1, ช่วงอันดับ 5–6  
**Pressure:** สูง

**คู่แข่งหลัก**

- Platform Wongwian Yai — ประมาณ 0.20 กม.
- ICS — ประมาณ 1.41 กม.; นับรวม cluster กับ ICONSIAM
- SENA Fest — ประมาณ 1.51 กม.
- ICONSIAM — ประมาณ 1.66 กม.; destination cluster
- The Mall Lifestore Tha Phra — ประมาณ 2.11 กม.

**สิ่งที่ต้องเป็นจริง**

มีแปลงที่ access/visibility เหนือกว่า Platform และจับ routine คนพื้นที่ที่ destination cluster ไม่ตอบ

**Kill test**

หากแปลงที่เป็นไปได้ไม่มี friction advantage ให้ลดลำดับ แม้ baseline จะนิ่ง

### 5.7 บางขุนนนท์-ใต้

**Fresh signal:** อันดับ 7, คะแนน 84.7, ช่วงอันดับ 7–11  
**Pressure:** สูงมากระดับภูมิภาค

**คู่แข่งหลัก**

- Central Pinklao — ประมาณ 2.02 กม.; Retail NLA 64,917 ตร.ม.; renovation ล่าสุดเพิ่ม food, fashion, sport และ new formats
- Lotus’s Merry King Pinklao — ประมาณ 2.02 กม.; current branch verified; GLA unknown
- The Sense Pinklao — current community/lifestyle mall; current GLA และ coordinate lineage ยังไม่พอสำหรับ size-scaled marker
- Meeting Mall อยู่ Bang O/Charan 94 ไม่ควรถูกนับเป็น direct pressure จนกว่า routing ยืนยัน

**โอกาสที่ยังพอมี**

ไม่ใช่ white space ระดับ regional shopping แต่มีสมมติฐานว่า neighbourhood access, short visit, pet/family routine หรือ food/wellness ที่เข้าถึงเร็วกว่า Central อาจยังไม่ถูกตอบ

**Kill test**

หยุดหากคลอง รถไฟ การกลับรถ หรือ parcel access ทำให้เส้นทางใช้งานจริงแย่กว่าศูนย์เดิม

### 5.8 แยกบ้านแขก

**Fresh signal:** อันดับ 8, คะแนน 84.0, ช่วงอันดับ 6–31  
**Pressure:** กลาง–สูง / route-sensitive

**คู่แข่งหลัก**

- Platform Wongwian Yai — ประมาณ 0.79 กม.
- The Old Siam Plaza — ประมาณ 1.67 กม.; heritage/craft/traditional food niche; route/crossing required
- ICS — ประมาณ 2.00 กม.; cluster with ICONSIAM
- ICONSIAM — ประมาณ 2.21 กม.
- SENA Fest — ประมาณ 2.37 กม.
- The Mall Lifestore Tha Phra — ประมาณ 2.53 กม.

**สิ่งที่ต้องเป็นจริง**

คะแนน routine สูงต้องแปลเป็น stop-and-stay demand ไม่ใช่คนผ่าน และต้องไม่ซ้ำกับตลาดพลู/สำเหร่/วงเวียนใหญ่

**Kill test**

หากอันดับยังแกว่งหลังใช้ network และ overlap สูง ให้ตัดก่อนเข้าสู่ parcel search

### 5.9 บางโพ-ตะวันออก

**Fresh signal:** อันดับ 9, คะแนน 83.1, ช่วงอันดับ 9–18  
**Pressure:** สูง

**คู่แข่งหลัก**

- Gateway at Bangsue — ประมาณ 0.08 กม. จาก reference point
- Lotus’s Prachachuen — ประมาณ 1.13 กม.
- Meeting Mall — ประมาณ 1.35 กม. ระยะตรง แต่คนละฝั่ง/route context ต้องยืนยัน
- Central Ladprao — ประมาณ 4.12 กม.; route-dependent

**สิ่งที่ต้องเป็นจริง**

reference point ใกล้ Gateway มากผิดปกติ จึงต้องพิสูจน์ locale extent และ candidate parcel ก่อน หากเป็นเพียง demand signal รอบศูนย์เดิม ไม่ใช่ white-space opportunity ต้องลดลำดับ

**Kill test**

หากไม่มี site pocket ที่พ้น direct Gateway catchment ให้เก็บเป็น evidence ของตลาดแข็งแรง ไม่ใช่ development opportunity

### 5.10 พระราม 3-ตะวันออก

**Fresh signal:** อันดับ 10, คะแนน 82.9, ช่วงอันดับ 7–15; out-of-home 97.3  
**Pressure:** สูงมาก

**คู่แข่งหลัก**

- Central Rama 3 — ประมาณ 1.62 กม.; Retail NLA 48,328 ตร.ม.; nature/urban, food, coworking, kids, education และ fitness
- Bangkok Square Rama 3 — ประมาณ 2.03 กม.; F&B/community complex; current GLA unknown
- KINGSQUARE Community Mall — ประมาณ 2.22 กม.
- Terminal 21 Rama 3 — ประมาณ 4.50 กม.; route-dependent; historic 42,000 ตร.ม. retail area ไม่ใช่ current as-built GLA

**หลักฐาน weakness ที่ใช้ได้อย่างระวัง**

รายงานประชุมผู้ถือหุ้น LH เดือนพฤษภาคม 2026 ระบุว่า food court ทำหน้าที่ดึง traffic และอยู่ใกล้ break-even ขณะที่ศูนย์มี EBITDA เป็นบวกแต่ยังต้องใช้เวลาปรับ performance/valuation ก่อนขายเข้า REIT ข้อมูลนี้ **ไม่เท่ากับ** ศูนย์ล้มเหลว แต่ทำให้สมมติฐานเรื่อง format/food economics ควรถูกทดสอบ

**สิ่งที่ต้องเป็นจริง**

ข้อเสนอ PARC ต้องชนะด้วย low-rise, fast access, repeat routine และ curated choice ไม่ชน regional mall แบบตรง ๆ

**Kill test**

หยุดหาก customer interviews ไม่พบ friction หรือ unmet job ที่ชัดกว่าศูนย์เดิม

---

## 6. กติกาคู่แข่งสำหรับรอบละเอียด

### 6.1 หนึ่งทะเบียน หนึ่ง snapshot

ทุก locale ใช้ competitor registry release และ `as_of` เดียวกัน โดยมีอย่างน้อย:

- `competitor_id`
- canonical name / aliases
- operating status + as-of
- coordinate + source + confidence
- venue type / parent cluster
- Retail NLA หรือ GLA + definition + source + as-of ถ้ามี
- tenant count เฉพาะเมื่อเป็น current occupied-tenant audit และมี definition ชัด
- source URLs และ rights status

### 6.2 Unknown ไม่เท่ากับศูนย์

- ไม่ใช้ค่า NLA proxy ใน Venue Fundamental เป็น current verified GLA โดยอัตโนมัติ
- ไม่ใช้ total project area, GFA หรือ construction area แทน Retail NLA
- ไม่ใช้จำนวนรายการใน directory แทน occupied tenant count
- หาก size ไม่ทราบ ให้แสดง `ขนาดยังไม่ยืนยัน`
- ในแบบจำลองให้ทำ small / medium / large sensitivity แทนการสร้างตัวเลข

### 6.3 Cluster deduplication

- ICONSIAM + ICS นับเป็น destination cluster เดียวใน pressure aggregation
- ศูนย์ที่อยู่ในโครงการ/ownership cluster เดียวกันต้องมี `parent_cluster_id`
- map แสดงได้หลาย marker แต่ score ต้องลดการนับซ้ำ

### 6.4 High competition ไม่ใช่ automatic reject

ให้แยกสองแกน:

1. `competitor_supply_pressure` — มี supply ที่ลูกค้าเข้าถึงได้มากแค่ไหน
2. `strategic_gap_potential` — มี unmet job ที่พิสูจน์จาก field/source evidence หรือไม่

ทำเลที่ pressure สูงอาจไปต่อได้ หาก gap ชัดและ J มี capability ชนะจริง

---

## 7. แผนงานที่ขออนุมัติ

### Workstream A — route and market

- สร้าง 10/15/20 minute catchments สำหรับ car, motorcycle และ walk+transit
- ทำ weekday AM, weekday PM และ weekend
- ใช้ crossing registry สำหรับสะพาน ท่าเรือ ทางด่วน รถไฟ และคลอง
- คำนวณ overlap ภายใน 3 กลุ่มตลาด
- เลือกตัวแทนสูงสุดหนึ่งรายต่อ market cluster ก่อน final rank

### Workstream B — competitor census

- สำรวจคู่แข่งที่อยู่ใน route catchment เดียวกันให้ครบ
- ยืนยัน status, entrance, parking, NLA/GLA, anchor, offer, daypart และ experience
- ทำ weakness interview โดยไม่สรุปจาก online rating เพียงอย่างเดียว
- แยก operating supply ออกจาก pipeline

### Workstream C — customer and proposition

- ทดสอบ 3 jobs หลักไม่เกิน 3 ICP
- ตรวจ intent, visit duration, daypart และ willingness to switch
- ทดสอบ “Regular Refuge” กับ competitor reality
- ห้ามใช้ green/pet/wellness เป็นจุดต่างถ้าคู่แข่งทำได้อยู่แล้ว

### Workstream D — parcel and economics

- access, ingress/egress, visibility, turning, parking, flood, zoning และ utilities
- rent/land sensitivity
- concept size, tenant mix และ phasing
- downside scenario เมื่อคู่แข่งเพิ่มหรือเดินทางสะดวกขึ้น

### Board gate หลังจบรอบ

ส่งกลับ Board ด้วย:

- 10 locale dossiers
- 3 market-cluster decisions
- shortlist ไม่เกิน 3–5 investment candidates
- stop reasons สำหรับ locale ที่ตัด
- economics range และ evidence gaps

---

## 8. UX/UI Brief สำหรับ single-page HTML

### 8.1 Narrative

ลำดับการอ่าน:

1. **Decision hero** — “10 ทำเล / 1 การอนุมัติ / 3 kill tests”
2. **What changed** — คู่แข่งเปลี่ยนความหมายของ Fresh rank อย่างไร
3. **Explore Top 10** — filter + shortlist cards
4. **Overview map** — สถานะ 10 ทำเลและ market clusters
5. **Candidate map** — competitor markers + clickable detail
6. **Cluster choices** — ทำเลใดต้องแข่งกันเอง
7. **Evidence boundary** — อะไรรู้ / อะไรยังไม่รู้
8. **Decision CTA** — อนุมัติศึกษารายละเอียด Top 10

### 8.2 CTA contract

Primary CTA:

> **อนุมัติศึกษารายละเอียด Top 10**

Support copy:

> ตรวจเส้นทาง คู่แข่ง ความต้องการลูกค้า แปลง และ economics เพื่อกลับมาพร้อม shortlist 3–5 ทำเล—ยังไม่ใช่อนุมัติลงทุน

Secondary CTA:

- ดูขอบเขตงานที่อนุมัติ
- ดาวน์โหลดรายงานวิเคราะห์

CTA scope ต้องผูกกับ candidate IDs ทั้ง 10 เท่านั้น และห้ามมีคำว่า “อนุมัติ 745” ใน decision surface

### 8.3 Map contract

#### Overview

- ใช้ clean SVG
- แสดง reference points 10 จุด
- แสดง 3 market clusters ด้วยเส้น/พื้นที่เบา
- แสดง simplified orientation basemap ที่ไม่อ้างว่าเป็นเขตทางกฎหมาย
- ไม่แสดง decorative dots
- มี north, scale และ fallback table

#### Candidate detail

- ห้ามวาดวงกลมเป็น locale extent
- เมื่อ polygon source ยังไม่มี ให้แสดง `locale extent unavailable` อย่างชัดเจน
- ใช้ reference point + metric grid + north + 1 กม. scale
- competitor marker ทุกจุดมี ID, name, status, impact class, size basis, source status
- click/tap/Enter เปิด detail; Escape ปิดและคืน focus
- มี fallback competitor list เสมอ

#### Marker sizing

ขนาด marker ใช้ **verified impact class** ชุดเดียว:

- High
- Medium-high
- Medium

ถ้ามี current verified Retail NLA ให้แสดงตัวเลขใน detail และใช้เป็นหนึ่งในหลักฐานจัด class  
ถ้าไม่มี ให้แสดง `size unknown` และอธิบาย basis  
ไม่ผสม tenant count กับ sqm ใน scale เดียว

### 8.4 Visual system

- Canvas `#F7F2E9`
- Card `#FFFDF8`
- Ink `#24312F`
- Garden `#365E55`
- Bougainvillea `#A94372`
- Petal Mist `#F3E0E8`
- Sage Mist `#DDE5DE`
- Control border `#85776C`
- Focus ring 3px `#A94372`

Typography:

- Anuphan readable heading; production patch ใช้น้ำหนัก 300 เมื่อไฟล์ 200 ไม่พร้อม
- IBM Plex Sans Thai Looped 400 สำหรับเนื้อหา
- IBM Plex Sans Thai Looped 500 สำหรับ control/CTA
- body 18px ขึ้นไป, UI 16px ขึ้นไป, target 44px ขึ้นไป

### 8.5 Bougainvillea motif

ระดับความดัง: **Q1 — quiet**

- ใช้ original Bézier geometry เท่านั้น
- หนึ่ง branch fragment หรือ 2–3 abstract bracts ต่อหนึ่ง narrative flight
- อยู่ขอบ composition และไม่แตะ CTA safe zone
- ใช้ Petal Mist + Bougainvillea ในสัดส่วนต่ำกว่า 5% ของ viewport
- ความเงียบเกิดจากพื้นที่ว่าง สเกล และ saturation—not opacity ของข้อความ
- ภาพอ้างอิงที่แนบมาใช้ดูจังหวะพฤกษศาสตร์เท่านั้น ไม่ crop, trace หรือวางใน production

### 8.6 Interaction ที่ต้องมี

- filter: All 10 / Prove first / Cluster decision / Highest hurdle
- progress indicator ว่า explore แล้วกี่แห่ง
- detail drawer ต่อ locale
- competitor marker detail
- “Mark as reviewed” state ใช้ shape/check + text ไม่ใช้สีอย่างเดียว
- sticky decision dock แสดง scope “10/10”
- light/dark/system control แบบ quiet icon
- `prefers-reduced-motion`
- print view ที่ยังอ่านคำตัดสิน ตาราง และ sources ได้

---

## 9. Data and geometry disclosure

### Candidate reference points

Fresh HTML v1.0 มี presentation points แต่ไม่ได้ส่ง polygon geometry มาในไฟล์แนบ  
รอบนี้ใช้ reference coordinates จากการแปลงตำแหน่ง Fresh SVG ด้วย WGS84 calibration points ที่ใช้ชื่อ locale เดียวกันใน release audit เดิม

- residual ของจุด calibration ต่ำมากพอสำหรับ orientation map
- จุดดังกล่าว **ไม่ใช่ parcel centroid**
- จุดดังกล่าว **ไม่สร้าง locale polygon**
- ห้ามใช้จุดดังกล่าวตัดสิน catchment หรือ parcel

### Competitor coordinates

ใช้พิกัดจาก Venue Locale Fundamental registry สำหรับ presentation map โดย:

- แสดง source/confidence ใน data payload
- สถานะเปิดบริการตรวจด้วย operator/official sources
- ไม่ใช้ Google/Longdo tenant proxy point เป็น host centroid
- venue ที่ coordinate lineage ไม่พอถูกเก็บใน detail list แต่ไม่วาด marker

### Simplified basemap

เนื่องจากไม่มี approved khwaeng geometry ใน release นี้:

- HTML ใช้ metric grid และ orientation labels เป็น fallback ที่ประกาศชัด
- ไม่วาด polygon ปลอม
- ไม่อ้างว่าเป็นแนวเขตทางกฎหมาย
- เมื่อได้รับ approved GeoJSON/WKT จึงเปิด administrative boundary layer ใน release ถัดไป

---

## 10. Evidence register

### Project and internal sources

- `PARC_Bangna_Fresh_Locale_Screen_Analysis_and_UXUI_Brief_v0.1_2026-07-28.md`
- `PARC_Bangna_Bangkok_Top_10_Release_1_5_Analysis_and_UXUI_2026-07-27.md`
- `venue_locale_fundamental_data_audit_v0_1_2026-07-27.md`
- Venue Locale Insight registry v2.3.1
- Venue Locale Fundamental v0.2.0-rc1, release candidate
- GitHub audit history: Release 1.6 competitor registry and map contract

### Operator and primary sources

- [Central Pattana retail properties asset table](https://www.centralpattana.co.th/en/investor-relations/assets-under-central-pattana/retail-properties)
- [Central EastVille branch](https://shoppingcenter.centralpattana.co.th/branch/central-eastville/branch-information)
- [Central Rama 3 branch](https://shoppingcenter.centralpattana.co.th/branch/central-rama-3/branch-information/)
- [The Crystal Ekamai-Ramindra — ALLY REIT](https://www.allyreit.com/en/portfolio/29/the-crystal-ekamai-ramindra)
- [Crystal Design Center — ALLY REIT](https://www.allyreit.com/en/portfolio/20/crystal-design-center)
- [Gateway at Bangsue — AWC](https://www.assetworldcorp-th.com/en/portfolio/retails-and-wholesales/79/gateway-at-bangsue)
- [Lotus’s Prachachuen branch 5030](https://my.lotuss.com/branch/5030/en)
- [Lotus’s Merry King Pinklao branch 5068](https://my.lotuss.com/branch/5068/en)
- [The Sense Pinklao](https://www.thesensebkk.com/)
- [The Mall Lifestore Tha Phra](https://themalllifestore.com/branch/thapra)
- [SENA Fest project information](https://www.senafest.com/en/about)
- [SENA Development One Report 2025](https://www.sena.co.th/content/files/56-1-report/2026/Apr/1004/SENA-e-one-Report-2568_090469_EN_compressed.pdf)
- [Terminal 21 Rama 3 floors](https://www.terminal21.co.th/rama3/en/staticblocks/floor-home-en/)
- [Terminal 21 Rama 3 directory](https://www.terminal21.co.th/rama3/en/shop-categories-en/home-en2/)
- [Land & Houses AGM 2026 minutes](https://investor.lh.co.th/storage/downloads/shareholders-meeting/agm2026/20260522-lh-agm2026-minutes-en.pdf)
- [The Old Siam Plaza](https://theoldsiam.co.th/en/)

### Evidence boundary

- Operator facts support status, programme and disclosed metrics only
- Field observation is still required for access, weakness, occupancy, traffic and service quality
- Venue Fundamental RC1 is a discovery/index layer, not a complete operating census
- Redistribution rights for derived registry fields remain subject to release review

---

## 11. Approval wording

### Board resolution draft

> อนุมัติให้ฝ่ายบริหารดำเนินการศึกษารายละเอียด Top 10 ทำเลจาก PARC Bangna Fresh Locale Screen ครบทั้ง 10 แห่ง โดยครอบคลุม route-based catchment, competitor census, customer unmet jobs, market overlap, candidate parcel access และ preliminary economics เพื่อกลับมาเสนอ shortlist ไม่เกิน 3–5 ทำเลพร้อม stop reasons และ downside scenarios ทั้งนี้การอนุมัติครั้งนี้ไม่ใช่การอนุมัติเลือกทำเล ซื้อที่ดิน หรืออนุมัติลงทุนโครงการ

---

## 12. Final working rule

> **Approve ten investigations, not ten investments.**  
> ให้คู่แข่งเป็นตัวทดสอบความต่าง ให้เส้นทางจริงเป็นตัวตัดตลาด และให้แปลงกับ economics เป็นด่านสุดท้ายก่อนลงทุน
