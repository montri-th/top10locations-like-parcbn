# PARC Bangna — Bangkok Top 10 Location Screening

## Release 1.6: Competition Overlay + UX/UI Specification

**วันที่หลักฐาน:** 28 กรกฎาคม 2026
**ฐานอันดับหลัก:** Release 1.5
**Locale Insight release:** `venue-locale-insight-v2.3.1`
**หน่วยวิเคราะห์:** catchment พื้นที่เท่ากัน 26.3154 ตร.กม. รอบ candidate center รัศมี 2.89421 กม.
**สถานะรายงาน:** ผลวิเคราะห์, data contracts, HTML และ pre-publish rendered QA ของ Release 1.6 ผ่านแล้ว; รอเผยแพร่และ post-publish QA ก่อนประกาศ release status `PASS`

> เอกสารนี้คงอันดับหลักและคะแนน Release 1.5 เพื่อรักษา comparable baseline แล้วเพิ่มชั้นวิเคราะห์ “แรงกดดันจากคู่แข่ง” และ “ช่องว่างเชิงกลยุทธ์” เป็น diagnostic สำหรับเปลี่ยนลำดับการลงมือ ไม่ใช้รายชื่อคู่แข่งเบื้องต้นไปสร้างอันดับใหม่อย่างมั่นใจเกินหลักฐาน

---

## 1. Executive verdict

### 1.1 คำตัดสินหลัก

อันดับ Top 10 หลักยังคงตาม Release 1.5:

1. วงเวียนใหญ่–ตะวันออก — 52.71
2. เจริญราษฎร์ — 52.61
3. สำเหร่ — 52.31
4. แยกบ้านแขก — 51.46
5. ตลาดพลู–ใต้ — 48.44
6. บางปะกอก — 47.02
7. วังหลัง — 45.74
8. ราชเทวี — 44.14
9. ประชาอุทิศ — 43.78
10. ดินแดง — 43.57

การแข่งขันเปลี่ยนความหมายของอันดับอย่างมีนัยสำคัญ:

- **วงเวียนใหญ่–ตะวันออก** ยังเป็น baseline อันดับ 1 แต่มี verified competitor 7 แห่ง, competitive supply pressure แตะเพดานโมเดล และ `competitive room = 7.50` จึงไม่ควรเดินหน้าจากคะแนนทำเลอย่างเดียว
- **เจริญราษฎร์** ยังเป็น baseline อันดับ 2 แต่ KINGSQUARE Community Mall อยู่ 1.231 กม. และมี mission overlap โดยตรงกับ community/family/routine concept จึงต้องพิสูจน์จุดต่างก่อนคัดแปลง
- **สำเหร่** ต้องหยุดและยืนยัน candidate center ก่อน เพราะจุดวิเคราะห์อยู่ห่าง Riverside Plaza เพียง 0.034 กม. ซึ่งอาจหมายถึง candidate-center artifact ไม่ใช่โอกาสพัฒนาอิสระ
- **บางปะกอก** เป็นทำเลเดียวที่ได้ Action Tier A ใน overlay รอบนี้: baseline ยังแข่งขันได้ที่ 47.02, `competitive room = 47.04` และ `evidence readiness = 85` แต่ยังต้องตรวจ registry ให้ครบและพิสูจน์ leakage ไป Terminal21 Rama 3
- **วังหลัง** และ **ประชาอุทิศ** ดูมี competitive room สูง แต่หลักฐานยังไม่พร้อมพอให้เลื่อนเป็นอันดับหลัก: วังหลังยังไม่คิดผลของแม่น้ำ/เรือ/สะพาน ส่วนพิกัด Market Place Pracha Uthit ยังเป็น tenant-in-mall proxy
- **ราชเทวี** และ **ดินแดง** อยู่ในกลุ่มการแข่งขันสูงมาก; ควรเดินหน้าต่อเฉพาะเมื่อมี parcel right, micro-format หรือจุดต่างที่พิสูจน์ได้

### 1.2 ลำดับงานที่แนะนำ

1. **บางปะกอก — ตรวจเชิงรุก:** ทำ full competitor census, network catchment, evening stop-rate และ leakage study
2. **วงเวียนใหญ่–ตะวันออก + เจริญราษฎร์ — competition-first gate:** ตรวจ access, tenant overlap, routine overlap และ economics ก่อนเพิ่มค่าใช้จ่ายด้าน parcel
3. **สำเหร่ — geometry gate:** ยืนยัน source polygon/parcel และ recenter ก่อนวิเคราะห์ต่อ
4. **วังหลัง + ประชาอุทิศ — evidence gate:** ตรวจ river impedance หรือ host centroid ตามกรณีก่อนให้ competitive room มีผลต่ออันดับ
5. **ราชเทวี + ดินแดง — de-prioritize:** เก็บไว้เฉพาะกรณี format หรือสิทธิ์ไซต์เปลี่ยนโจทย์

### 1.3 สิ่งที่ยังไม่ใช่ข้อสรุป

- ไม่ได้สรุปว่าคู่แข่งรายใด occupancy ต่ำ, tenant mix อ่อน, traffic ต่ำ, บริการไม่ดี หรือ underperform
- ไม่ได้สรุปว่าพื้นที่ที่มีคู่แข่งน้อยคือ white space โดยอัตโนมัติ
- ไม่ได้ใช้ proxy GLA หรือ nearby-POI count เป็น GLA/tenant count จริง
- ไม่ได้ใช้ระยะเส้นตรงแทนเวลาเดินทางจริงเมื่อมีแม่น้ำ สะพาน เรือ หรือโครงข่ายถนน
- ไม่ได้ตีความ candidate center เป็นตำแหน่งแปลงหรือขอบเขตกฎหมาย

---

## 2. Decision boundary

### คะแนนและ overlay นี้ใช้ได้กับ

- คัดลำดับพื้นที่สำหรับ field validation
- ระบุว่าทำเลใดต้องผ่าน competition, geometry, network หรือ evidence gate ก่อน
- ตั้งสมมติฐาน strategy ที่ต้องพิสูจน์กับคู่แข่งจริง
- เปรียบเทียบ 10 catchments ภายใต้ release และกติกาพื้นที่เดียวกัน
- เตรียมโจทย์ parcel search และ consumer/competitor fieldwork

### คะแนนและ overlay นี้ยังใช้ไม่ได้กับ

- อนุมัติซื้อที่ดินหรือเซ็นสัญญาเช่า
- ประมาณยอดขาย footfall หรือ market share
- อ้าง current occupancy, current tenant count หรือ performance ของคู่แข่ง
- ตัดสินรูปแบบโครงการโดยไม่เห็นแปลง ทางเข้า–ออก ที่จอดรถ servicing และ economics
- สรุป final rank จาก scenario 80/20

---

## 3. Concept contract และ site firewall

### 3.1 แหล่งควบคุม concept

แก่น concept มาจาก `Project brief - PARC Bangna(1).md` เท่านั้น ส่วน J Lifestyle Center Design System v0.3 ควบคุมการนำเสนอ ไม่ใช้เป็น evidence ด้าน demand

ข้อมูลของ PARC Samyot, LIVE Ramintra หรือโครงการอื่นไม่ถูกนำมาเป็น operating evidence, active locale, persona, tenant performance หรือ demand fact ของ candidate ทั้ง 10 แห่ง

### 3.2 แก่นแนวคิดที่ถ่ายโอนได้

| Principle | ความหมายต่อการคัดทำเล | ข้อจำกัด |
|---|---|---|
| Routine-led neighborhood center | สร้าง repeat visit จาก routine รายสัปดาห์ ไม่พึ่ง destination traffic เพียงอย่างเดียว | ไม่โอน observed frequency หรือ performance จาก PARC Bangna |
| Food as entry, not the whole concept | อาหารเป็นเหตุผลแรกได้ แต่ต้องเชื่อม next stop ระหว่าง tenant | ไม่โอนรายชื่อร้านหรือ tenant economics |
| Calm connected place | ความสงบ เดินง่าย และ journey ที่ต่อกันเป็นช่องว่างที่ concept ต้องพิสูจน์ | landscape และ architecture ต้องตอบ parcel จริง |
| Competition as pressure and gap | คู่แข่งที่รับ routine เดียวกันลด room; คู่แข่งแบบ destination/specialist อาจเปิดช่องให้ routine-led format | “จุดอ่อนคู่แข่ง” ยังเป็น hypothesis จนกว่าจะตรวจภาคสนาม |

### 3.3 Site-specific facts ที่ห้ามถ่ายโอน

- tenant roster ของ PARC Bangna
- access, visibility, parking และ traffic ของ PARC Bangna
- operating performance หรือ commercial performance ของ PARC Bangna
- customer journey ที่ยังเป็น strategic recommendation ไม่ใช่ observed behavior

### 3.4 Strategy ที่ใช้เป็น hypothesis ได้

- **Regular Refuge for Quality Everyday Life**
- routine ระยะประมาณ 60–120 นาที
- curated choice แทนการแข่งด้วย scale
- family, self-care และ pet-as-family เป็น mission territories
- calm atmosphere + tenant connection เป็น moat

ทุกข้อข้างต้นต้องทดสอบใหม่ในพื้นที่เป้าหมาย ไม่ใช่ assumption ที่ติดไปกับชื่อ concept

---

## 4. Data lineage และ evidence policy

### 4.1 ชั้นข้อมูล

| ชั้นข้อมูล | หน้าที่ | สถานะ |
|---|---|---|
| Release 1.5 opportunity score | comparable baseline ของ 10 ทำเล | คงไว้โดยไม่แก้คะแนน |
| Venue Locale Insight v2.3.1 | locale/catchment inputs | ใช้ release เดียวกันทุก candidate |
| Competitor registry v0.1.0-preliminary | identity, operating status, coordinates, operator metrics และ sources | minimum verified supply; ยังไม่ใช่ completeness-certified census |
| Competitor score breakdown | pressure, headroom, strategic gap, competitive room และ action tier | derived diagnostic |
| External operator/owner sources | ยืนยันสถานะและ metric ราย venue | ให้ความสำคัญเหนือ proxy |
| J Lifestyle Center Design System v0.3 | typography, colour, interaction, contrast และ visual restraint | presentation contract |

### 4.2 เหตุผลที่ไม่ใช้ Venue registry proxy เป็นขนาดจริง

จาก `venue_locale_fundamental_data_audit_v0_1_2026-07-27.md`:

- GLA ที่มี source จัดเป็น observed/external มีเพียง 329 แถว หรือ 3.0% ของทั้งชุด
- `gla_confidence` เป็น low, none หรือว่างรวม 10,494 แถว หรือ 96.5%
- `tenant_count` ที่มีค่า 10,397 แถว มี 10,354 แถว หรือ 99.6% เป็น nearby-POI count หรือค่าคำนวณ/default ไม่ใช่จำนวน tenant ที่ venue รายงาน

Release 1.6 จึงใช้ Venue registry เพื่อ entity resolution และพิกัดเป็นหลัก ส่วนขนาด marker ใช้ตามลำดับ:

1. operator-reported leasable area ที่นิยามชัด
2. operator-reported project/commercial area หรือ brand/shop capacity พร้อมแสดงชนิด metric
3. impact class ที่เปิดเผยว่าเป็น analytical classification

metric คนละชนิดจะไม่ถูกทำให้ดูเหมือนเป็น GLA เดียวกัน

### 4.3 Operating-supply scope

รวม:

- shopping center ที่เปิดให้บริการ
- lifestyle/community mall ที่เปิดให้บริการ
- department-store-led center ที่เปิดให้บริการ
- destination/specialty center ที่มีผลต่อ catchment

ไม่รวม:

- ตลาดดั้งเดิม ตลาดนัด ตลาดกลางคืน
- supermarket, convenience store หรือ retailer เดี่ยว
- โครงการ planned/under construction ที่ยังไม่มี operating evidence
- tenant-in-mall record ที่ซ้ำกับ host center
- King Power Rang Nam ในรอบนี้ เพราะยังไม่มี substitute-format policy ที่อนุมัติ

---

## 5. วิธีคำนวณ

### 5.1 Baseline Release 1.5

หน่วยวิเคราะห์ใช้ catchment พื้นที่เท่ากัน 26.3154 ตร.กม. รอบ restaurant-sample medoid ซึ่งไม่ใช่ source-polygon centroid หรือ parcel

\[
\text{Local Traffic}=0.50R+0.30V+0.20C
\]

โดย \(R\) คือ resident signal, \(V\) คือ visitor/outside signal และ \(C\) คือ daytime-origin proxy

\[
\text{Tenant Fit} =
0.40(\text{Food})+
0.20(\text{Routine})+
0.15(\text{Family})+
0.10(\text{Wellness})+
0.10(\text{Connector})+
0.05(\text{Pet-neutral})
\]

\[
\text{Experience Fit}
=0.35(\text{Residents})+
0.30(\text{Multi-mission})+
0.25(\text{Daypart})+
0.10(\text{neutral place-experience})
\]

\[
\text{Offering PMF}
=\text{Tenant Fit}^{0.60}\times \text{Experience Fit}^{0.40}
\]

\[
\text{Overall}
=\frac{\text{Catchment Traffic}\times\text{Offering PMF}}{100}
\]

ข้อจำกัดเดิมยังคงอยู่: Offering PMF ใช้ค่าของ seed locale ขณะที่ Traffic aggregate จาก locales ใน catchment และ missing บางประเภทในรุ่นเดิมยังถูกแทนด้วย zero

### 5.2 Competitor member load

impact class:

| Impact class | น้ำหนัก |
|---|---:|
| high | 5.0 |
| medium-high | 4.0 |
| medium | 3.0 |

proximity:

| ระยะเส้นตรง | น้ำหนัก |
|---|---:|
| ≤1.0 กม. | 1.00 |
| >1.0–2.0 กม. | 0.75 |
| >2.0–2.89421 กม. | 0.50 |

routine-overlap default:

| Venue type | Factor |
|---|---:|
| community mall | 1.00 |
| open-air shopping center | 0.90 |
| department-store-led shopping center | 0.80 |
| shopping center | 0.80 |
| destination shopping center | 0.55 |
| specialty shopping center | 0.55 |

\[
\text{Member Load}
=\text{Impact Weight}\times\text{Proximity Weight}\times\text{Routine-overlap Factor}
\]

Platform Wongwian Yai, Riverside Plaza, The Street Ratchada และบาง venue ใช้ overlap override ตาม proposition ที่บันทึกใน registry

### 5.3 Cluster deduplication

ICONSIAM–ICS และ Siam Piwat Siam cluster ยังคงแสดงเป็น POI แยกในแผนที่ แต่ไม่บวกแรงกดดันเต็มซ้ำกัน:

\[
\text{Cluster Load}
=\max(\text{Member Loads})+0.25\times\sum(\text{Member Loads ที่เหลือ})
\]

### 5.4 Supply pressure, strategic gap และ competitive room

\[
\text{Supply Pressure}
=\min\left(100,\frac{\text{Deduplicated Pressure Load}}{12}\times100\right)
\]

\[
\text{Supply Headroom}=100-\text{Supply Pressure}
\]

Strategic gap เริ่มจาก 55 แล้วใช้ calibration heuristic:

- direct routine competitor ภายใน 2 กม.: −20
- direct routine competitor ใน outer catchment: −10
- competitor ใกล้กว่า 300 เมตร: −10
- สำเหร่เกือบตรง Riverside Plaza: −10
- destination/specialist load มากกว่าหรือเท่ากับ 60% ของ member load: +10
- จำกัดช่วง 20–70

Strategic gap ทุกค่ามีสถานะ **hypothesis** ไม่ใช่ observed unmet demand

\[
\text{Competitive Room}
=0.70(\text{Supply Headroom})+0.30(\text{Strategic Gap})
\]

เหตุผลที่ headroom มีน้ำหนักมากกว่า: evidence เรื่อง “มีคู่แข่งที่เปิดอยู่” แข็งกว่าข้อสันนิษฐานเรื่อง “จุดอ่อนหรือช่องว่าง” ของคู่แข่ง

### 5.5 Evidence readiness

เริ่มที่ 85 เพราะ registry ยังเป็น preliminary minimum verified supply แล้วลดเพิ่มเมื่อ:

- candidate center มี artifact
- river/bridge/ferry network ยังไม่ถูก model
- dense cluster ยังไม่ complete
- host centroid ใช้ tenant-in-mall proxy

Evidence readiness ไม่ถูกใช้เพิ่ม opportunity score

### 5.6 Action tier

| Tier | กติกา | ความหมาย |
|---|---|---|
| A | competitive room ≥45 และ readiness ≥80 | เดินหน้าตรวจทำเลเชิงรุก |
| B | competitive room ≥45 และ readiness <80 | มีช่องว่าง แต่ต้องยืนยันภาคสนามก่อน |
| C | 20≤ competitive room <45 | พิจารณาเฉพาะ strategy ที่ต่างจากคู่แข่งชัด |
| D | competitive room <20 | แข่งขันสูง; เดินหน้าต่อเมื่อมีสิทธิ์ไซต์หรือจุดต่างเหนือกว่า |

Action tier เป็น decision gate ไม่ใช่อันดับใหม่

---

## 6. ผลหลัก: Canonical Top 10 + competition diagnostic

| # หลัก | ทำเล | Baseline | คู่แข่งยืนยันในวง | Pressure | Competitive room | Evidence readiness | Action tier |
|---:|---|---:|---:|---:|---:|---:|---|
| 1 | วงเวียนใหญ่–ตะวันออก | **52.71** | 7 | 100.00 | **7.50** | 85 | **D** |
| 2 | เจริญราษฎร์ | **52.61** | 4 | 84.17 | **21.58** | 85 | **C** |
| 3 | สำเหร่ | **52.31** | 5 | 100.00 | **6.00** | 65 | **D** |
| 4 | แยกบ้านแขก | **51.46** | 7 | 100.00 | **10.50** | 65 | **D** |
| 5 | ตลาดพลู–ใต้ | **48.44** | 3 | 80.21 | **24.35** | 85 | **C** |
| 6 | บางปะกอก | **47.02** | 2 | 52.08 | **47.04** | 85 | **A** |
| 7 | วังหลัง | **45.74** | 3 | 40.73 | **54.99** | 65 | **B** |
| 8 | ราชเทวี | **44.14** | 6 | 100.00 | **16.50** | 70 | **D** |
| 9 | ประชาอุทิศ | **43.78** | 1 | 20.83 | **68.92** | 65 | **B** |
| 10 | ดินแดง | **43.57** | 9 | 100.00 | **13.50** | 70 | **D** |

### วิธีอ่านตาราง

- Baseline rank ยังคงบอก catchment opportunity + concept fit ภายใต้กติกา Release 1.5
- Pressure บอกแรงกดดันจาก minimum verified operating supply ภายใต้ heuristic ปัจจุบัน
- Competitive room บอกพื้นที่เชิงวิเคราะห์ที่เหลือหลัง pressure และ strategic-gap hypothesis
- Evidence readiness บอกว่าควรเชื่อ diagnostic มากเพียงใด ไม่ใช่คุณภาพทำเล
- จำนวน venue เป็น individual verified POIs แต่ integrated clusters ถูก deduplicate ใน pressure score

---

## 7. Scenario 80/20 — illustrative, noncanonical

### 7.1 นิยาม

\[
\text{Illustrative Score}
=0.80(\text{Release 1.5 Baseline})+
0.20(\text{Competitive Room})
\]

scenario นี้ใช้เพื่อดูว่าการให้ competition มีน้ำหนักอาจเปลี่ยนลำดับอย่างไรเท่านั้น ไม่ใช่ final rank เพราะ:

- registry ยังไม่ completeness-certified
- river/network impedance ยังไม่ครบ
- strategic gap เป็น heuristic hypothesis
- candidate center บางแห่งยังต้อง recenter
- พิกัด host center บางแห่งยังเป็น proxy

### 7.2 ผล 80/20

| อันดับ scenario | ทำเล | Scenario score | อันดับหลัก | การเปลี่ยน |
|---:|---|---:|---:|---:|
| 1 | ประชาอุทิศ | **48.81** | 9 | +8 |
| 2 | วังหลัง | **47.59** | 7 | +5 |
| 3 | บางปะกอก | **47.02** | 6 | +3 |
| 4 | เจริญราษฎร์ | **46.40** | 2 | −2 |
| 5 | วงเวียนใหญ่–ตะวันออก | **43.67** | 1 | −4 |
| 6 | ตลาดพลู–ใต้ | **43.62** | 5 | −1 |
| 7 | แยกบ้านแขก | **43.27** | 4 | −3 |
| 8 | สำเหร่ | **43.05** | 3 | −5 |
| 9 | ราชเทวี | **38.61** | 8 | −1 |
| 10 | ดินแดง | **37.56** | 10 | 0 |

### 7.3 Sensitivity ของน้ำหนัก competition

เมื่อขยับเป็น 90/10:

1. เจริญราษฎร์
2. วงเวียนใหญ่–ตะวันออก
3. สำเหร่
4. แยกบ้านแขก
5. บางปะกอก
6. วังหลัง
7. ประชาอุทิศ
8. ตลาดพลู–ใต้
9. ราชเทวี
10. ดินแดง

เมื่อขยับเป็น 70/30:

1. ประชาอุทิศ
2. วังหลัง
3. บางปะกอก
4. เจริญราษฎร์
5. ตลาดพลู–ใต้
6. แยกบ้านแขก
7. วงเวียนใหญ่–ตะวันออก
8. สำเหร่
9. ราชเทวี
10. ดินแดง

ความเปลี่ยนแปลงกว้าง เช่น ประชาอุทิศอยู่ช่วงอันดับ 1–7 และวงเวียนใหญ่–ตะวันออกอยู่ช่วง 2–7 ภายใต้ weight sensitivity นี้ ยืนยันว่า 80/20 ต้องใช้เป็น **diagnostic scenario** ไม่ใช่ published primary rank

---

## 8. วิเคราะห์รายทำเล

### 8.1 วงเวียนใหญ่–ตะวันออก

**Baseline:** #1, 52.71
**Diagnostic:** 7 verified competitors · pressure 100.00 · room 7.50 · readiness 85 · **Tier D**

| คู่แข่ง | ระยะเส้นตรง | Impact |
|---|---:|---|
| Platform Wongwian Yai | 0.202 กม. | high |
| ICS Lifestyle Complex | 1.411 กม. | high |
| SENA Fest | 1.509 กม. | medium |
| ICONSIAM | 1.663 กม. | high |
| The Mall Lifestore Tha Phra | 2.108 กม. | high |
| Riverside Plaza Bangkok | 2.294 กม. | high |
| The Old Siam Plaza | 2.335 กม. | medium |

ICONSIAM และ ICS แสดงแยกเป็น POI แต่ถูก deduplicate เป็น cluster ใน pressure score

**คำวินิจฉัย**

baseline demand แข็ง แต่ Platform อยู่ใกล้มากและมี routine overlap สูง ขณะเดียวกัน catchment เชื่อมกับ destination และ full-format supply หลายแห่ง จึงไม่ควรสรุปว่าอันดับ 1 คือ development priority อันดับ 1

**Strategy hypothesis หากเดินหน้าต่อ**

ทดสอบ format ที่เล็กกว่า สงบกว่า และ routine-led กว่า destination centers แต่ห้ามอ้างว่า Platform หรือคู่แข่งรายใดทำเรื่องนี้ไม่ดีจนกว่าจะมี field evidence

**Gate**

- competitor journey/tenant-overlap audit
- access, parking, service circulation และ downside economics
- นับ routine 4 dayparts × weekday/weekend
- พิสูจน์ food → everyday service → short-pause café journey

### 8.2 เจริญราษฎร์

**Baseline:** #2, 52.61
**Diagnostic:** 4 verified competitors · pressure 84.17 · room 21.58 · readiness 85 · **Tier C**

| คู่แข่ง | ระยะเส้นตรง | Impact |
|---|---:|---|
| KINGSQUARE Community Mall | 1.231 กม. | high |
| Terminal21 Rama 3 | 1.484 กม. | high |
| Central Rama 3 | 2.272 กม. | high |
| SENA Fest | 2.731 กม. | medium |

Central Pattana รายงาน Central Rama 3 มี leasable area 48,328 ตร.ม. ณ 31 ธันวาคม 2024; metric นี้ใช้เป็น scale evidence ของ venue นั้น ไม่ถูกนำไปแทนขนาด venue อื่น

**คำวินิจฉัย**

KINGSQUARE เป็น direct community/family/routine overlap ทำให้ยังไม่มี clean strategic gap แม้ baseline จะสูงมาก Terminal21 และ Central Rama 3 เพิ่ม broader supply ใน catchment

**Strategy hypothesis หากเดินหน้าต่อ**

ต้องระบุ mission ที่ KINGSQUARE ไม่ได้เป็นเจ้าของ พร้อมแสดงว่าพื้นที่ใหม่มี access, parcel economics และ connected tenant journey ที่ดีกว่าพอให้ลูกค้าเปลี่ยน routine

**Gate**

- downside economics ก่อน traffic count ขนาดใหญ่
- compare tenant roster/adjacency และ arrival-to-second-stop journey
- family, self-care, pet routine switching interviews
- ห้ามตีความ “ขนาดเล็กกว่า” ว่า “อ่อนกว่า”

### 8.3 สำเหร่

**Baseline:** #3, 52.31
**Diagnostic:** 5 verified competitors · pressure 100.00 · room 6.00 · readiness 65 · **Tier D**

| คู่แข่ง | ระยะเส้นตรง | Impact |
|---|---:|---|
| Riverside Plaza Bangkok | **0.034 กม.** | high |
| The Mall Lifestore Tha Phra | 1.490 กม. | high |
| SENA Fest | 2.373 กม. | medium |
| Terminal21 Rama 3 | 2.403 กม. | high |
| Platform Wongwian Yai | 2.435 กม. | high |

**คำวินิจฉัย**

ระยะ 34 เมตรระหว่าง analytical center กับ Riverside Plaza เป็น decision-changing artifact: candidate อาจสะท้อน locale ของ incumbent center ไม่ใช่ development opportunity อิสระ

**Strategy**

ยังไม่ควรตั้ง strategy ต่อจาก center ปัจจุบัน

**Gate**

1. ขอ source polygon หรือ parcel candidate
2. recenter candidate
3. rerun catchment และ competitor overlay
4. หลังจากนั้นจึงตรวจ resident repeat, daytime bridge และ tenant journey

### 8.4 แยกบ้านแขก

**Baseline:** #4, 51.46
**Diagnostic:** 7 verified competitors · pressure 100.00 · room 10.50 · readiness 65 · **Tier D**

| คู่แข่ง | ระยะเส้นตรง | Impact |
|---|---:|---|
| Platform Wongwian Yai | 0.794 กม. | high |
| The Old Siam Plaza | 1.667 กม. | medium |
| ICS Lifestyle Complex | 2.000 กม. | high |
| ICONSIAM | 2.213 กม. | high |
| SENA Fest | 2.372 กม. | medium |
| Tha Maharaj | 2.380 กม. | medium |
| The Mall Lifestore Tha Phra | 2.531 กม. | high |

**คำวินิจฉัย**

fixed circle นับ supply ข้ามแม่น้ำโดยยังไม่คิดสะพาน เรือ เวลาเดินทาง หรือ pedestrian friction จึงอาจประเมิน overlap สูงเกินจริง แต่ Platform อยู่ฝั่งใกล้และเป็น direct routine pressure ที่ต้องตรวจจริง

**Strategy hypothesis หากเดินหน้าต่อ**

routine-led local offer อาจยังมี room หาก network access แยก demand ออกจาก destination cluster อย่างมีนัยสำคัญ

**Gate**

- bridge/ferry travel-time catchment
- Platform tenant/routine overlap
- after-school → dinner conversion
- parcel access และ parking

### 8.5 ตลาดพลู–ใต้

**Baseline:** #5, 48.44
**Diagnostic:** 3 verified competitors · pressure 80.21 · room 24.35 · readiness 85 · **Tier C**

| คู่แข่ง | ระยะเส้นตรง | Impact |
|---|---:|---|
| The Mall Lifestore Tha Phra | **0.508 กม.** | high |
| Riverside Plaza Bangkok | 1.988 กม. | high |
| Platform Wongwian Yai | 2.155 กม. | high |

**คำวินิจฉัย**

Offering PMF และ Experience Fit ของ baseline สูง แต่ The Mall Lifestore Tha Phra อยู่ใกล้มาก จึงไม่ควรเดินหน้าด้วย full-format copy ของ incumbent

**Strategy hypothesis หากเดินหน้าต่อ**

compact format ที่ curated และเชื่อม family meal → café/dessert → everyday goods ชัด อาจ defensible กว่า full-format offer

**Gate**

- tenant-overlap และ format sizing
- access/parking comparison กับ The Mall
- traffic 4 dayparts × weekday/weekend
- proof ว่า convenience/calm advantage สำคัญพอเปลี่ยน routine

### 8.6 บางปะกอก

**Baseline:** #6, 47.02
**Diagnostic:** 2 verified competitors · pressure 52.08 · room 47.04 · readiness 85 · **Tier A**

| คู่แข่ง | ระยะเส้นตรง | Impact |
|---|---:|---|
| Terminal21 Rama 3 | **0.845 กม.** | high |
| Riverside Plaza Bangkok | 2.829 กม. | high |

**คำวินิจฉัย**

minimum verified supply หนาแน่นน้อยกว่าหลาย candidate และข้อมูลพิกัดพร้อมกว่าเคส river/centroid artifact แต่ Terminal21 อยู่ใกล้และมี multi-category offer จึงยังห้ามสรุปว่าเป็น white space

**Strategy hypothesis**

ทดสอบ everyday routine, calm access และ evening repeat ที่ไม่ต้องแข่งขันด้วย destination scale

**Gate**

- complete shopping-center census
- network catchment และ leakage ไป Terminal21
- after-school–early evening stop rate
- parcel-level access, visibility, servicing และ economics

### 8.7 วังหลัง

**Baseline:** #7, 45.74
**Diagnostic:** 3 verified competitors · pressure 40.73 · room 54.99 · readiness 65 · **Tier B**

| คู่แข่ง | ระยะเส้นตรง | Impact |
|---|---:|---|
| Tha Maharaj | **0.251 กม.** | medium |
| The Old Siam Plaza | 1.792 กม. | medium |
| Central Pinklao | 2.756 กม. | high |

Central Pattana รายงาน Central Pinklao มี leasable area 64,917 ตร.ม. ณ 31 ธันวาคม 2024

**คำวินิจฉัย**

competitive room ดูสูง แต่ Tha Maharaj อยู่คนละฝั่งแม่น้ำและระยะเส้นตรง 251 เมตรไม่เท่ากับเวลาเดินทางจริง ค่า room จึงยังไม่พร้อมเลื่อนอันดับ

**Strategy hypothesis**

compact local format อาจมี room หาก ferry/bridge/pedestrian network แยก routine จริง แต่ full-format fit ยังต้องผ่าน access/parking gate

**Gate**

- ferry, bridge และ pedestrian travel time
- compact vs full-format economics
- parking turnover และ 60–120 minute dwell willingness
- complete venue/substitute census

### 8.8 ราชเทวี

**Baseline:** #8, 44.14
**Diagnostic:** 6 verified competitors · pressure 100.00 · room 16.50 · readiness 70 · **Tier D**

| คู่แข่ง | ระยะเส้นตรง | Impact |
|---|---:|---|
| Siam Discovery | 0.725 กม. | high |
| Siam Center | 0.760 กม. | high |
| Siam Paragon | 0.765 กม. | high |
| Platinum Fashion Mall | 0.891 กม. | high |
| centralWorld | 0.966 กม. | high |
| MBK Center | 0.987 กม. | high |

Siam Discovery, Siam Center และ Siam Paragon ถูก deduplicate เป็น Siam Piwat Siam cluster ใน pressure score. Central Pattana รายงาน centralWorld มี leasable area 180,386 ตร.ม. ณ 31 ธันวาคม 2024; Siam Paragon directory ระบุมากกว่า 300 brands ณ วันที่ตรวจ registry

**คำวินิจฉัย**

verified minimum set ทั้งหมดอยู่ในระยะประมาณ 1 กม. และ registry ยังไม่รับรองว่าครบ จึงควรให้ material competition penalty

**Strategy hypothesis หากเดินหน้าต่อ**

พิจารณาเฉพาะ micro-format, highly differentiated mission หรือ parcel right ที่ให้ข้อได้เปรียบเฉพาะ ห้ามแข่งด้วย broad mall proposition

**Gate**

- complete Siam–Ratchaprasong census
- parcel/access/economics เมืองชั้นใน
- mission-overlap study
- format proof ก่อน parcel search

### 8.9 ประชาอุทิศ

**Baseline:** #9, 43.78
**Diagnostic:** 1 verified competitor · pressure 20.83 · room 68.92 · readiness 65 · **Tier B**

| คู่แข่ง | ระยะเส้นตรง | Impact |
|---|---:|---|
| Market Place Pracha Uthit | 2.556 กม. | high |

Central Pattana ระบุ project area 8,600 ตร.ม., มากกว่า 40 brands, 3 ชั้น และที่จอดรถ 126 คัน ณ 29 พฤศจิกายน 2025; ตัวเลข expected 5,000 คน/วันในแหล่งเดียวกันเป็น forecast ไม่ใช่ observed footfall

**คำวินิจฉัย**

Market Place มี neighborhood/family/daily-convenience overlap โดยตรงกับ PARC-like routine concept แม้จะอยู่ outer catchment ส่วน competitive room สูงเกิดจาก minimum verified count เพียง 1 รายและห้ามตีความเป็น white space

พิกัด host center ปัจจุบันเป็น tenant-in-mall proxy จึงไม่ควร plot marker จนกว่าจะยืนยัน host centroid

**Strategy hypothesis**

ต้องหาความต่างที่ชัดกว่า “community convenience” และพิสูจน์ network catchment ว่า overlap จริงมากเพียงใด

**Gate**

- authoritative host centroid
- network catchment
- tenant/mission overlap
- complete competitor census
- แยก demand บ้าน/มหาวิทยาลัย/งานและตรวจ noon/after-school/evening

### 8.10 ดินแดง

**Baseline:** #10, 43.57
**Diagnostic:** 9 verified competitors · pressure 100.00 · room 13.50 · readiness 70 · **Tier D**

| คู่แข่ง | ระยะเส้นตรง | Impact |
|---|---:|---|
| Fortune Town | 1.268 กม. | high |
| Central Rama 9 | 1.369 กม. | high |
| Platinum Fashion Mall | 1.750 กม. | high |
| Esplanade Ratchada | 1.867 กม. | high |
| centralWorld | 2.046 กม. | high |
| Siam Paragon | 2.437 กม. | high |
| The Street Ratchada | 2.426 กม. | medium-high |
| Siam Center | 2.625 กม. | high |
| Siam Discovery | 2.727 กม. | high |

Central Pattana รายงาน leasable area ณ 31 ธันวาคม 2024: Central Rama 9 = 58,826 ตร.ม. และ Esplanade Ratchada = 42,401 ตร.ม. พิกัด Esplanade ใน registry ยังเป็น tenant-branch proxy จึงต้องยืนยัน host centroid ก่อน plot

**คำวินิจฉัย**

catchment ครอบคลุมทั้ง Rama 9–Ratchada และบางส่วนของ downtown cluster ทำให้ pressure สูง ขณะที่ census ยังไม่ complete และ baseline sensitivity เดิมกว้าง

**Strategy hypothesis หากเดินหน้าต่อ**

ต้องเป็น format ที่เฉพาะมากหรืออาศัย parcel/captive routine ที่ broad retail clusters ไม่ตอบ ไม่ควรใช้ PARC full-format proposition ไปชนตรง

**Gate**

- complete active-center census
- corridor/network relevance
- resident vs worker/daytime split
- micro-format and parcel economics

---

## 9. Portfolio sequencing หลังเพิ่ม competition

### Wave A — field priority

**บางปะกอก**

- complete competitor census
- network/access and leakage study
- evening routine validation
- parcel screen หลังผ่าน competition gate

### Wave B — baseline leaders with differentiation gate

**วงเวียนใหญ่–ตะวันออก + เจริญราษฎร์ + ตลาดพลู–ใต้**

- ไม่ยกเลิกจาก pipeline เพราะ baseline แข็ง
- ไม่เริ่มด้วย premise ว่า “ทำเลดีจึงลงได้”
- ต้องเริ่มจาก direct competitor audit, mission overlap และ parcel economics
- เดินหน้าต่อเฉพาะเมื่อ concept มีจุดต่างที่ผู้ใช้ให้คุณค่าจริง

### Wave C — evidence/geometry gate

**สำเหร่ + แยกบ้านแขก + วังหลัง + ประชาอุทิศ**

- สำเหร่: recenter
- บ้านแขก/วังหลัง: network catchment ที่คิดแม่น้ำ/สะพาน/เรือ
- ประชาอุทิศ: host centroid + complete registry

### Wave D — conditional only

**ราชเทวี + ดินแดง**

- เก็บไว้เมื่อมี micro-format, captive demand, strategic parcel หรือ economics ที่เปลี่ยนโจทย์
- ไม่ควรใช้ broad PARC-like offer ไปแข่งขันตรงกับ cluster ปัจจุบัน

---

## 10. Map และ geometry contract

### 10.1 Geometry ที่ต้องแยกจากกัน

| Geometry | ความหมาย | สถานะ Release 1.6 |
|---|---|---|
| Candidate center | restaurant-sample medoid จาก Release 1.5 | จุดอ้างอิงวิเคราะห์; ไม่ใช่ parcel |
| Standardized analytical catchment | วงรัศมี 2.89421 กม. / 26.3154 ตร.กม. | ใช้คำนวณและแสดงอย่างชัดว่าเป็น analytical extent |
| Competitor point | host venue point พร้อม source/confidence | แสดงเฉพาะพิกัดที่ผ่าน release gate |
| Source polygon | coordinate ring จาก source | ยังไม่มีในไฟล์ส่งมอบ |
| Evidence extent | รูปทรงอนุมานจาก sample | ไม่ใช้เป็น scored catchment หรือ parcel |
| Legal/parcel boundary | แนวเขตกฎหมาย/กรรมสิทธิ์ | ไม่มี |

### 10.2 หลักการแสดงแผนที่

- รักษาแผนที่ให้ clean และ quiet
- ไม่แสดงถนน รถไฟ หรือสถานีเมื่อไม่มี feature-level lineage ที่ตรวจได้
- ไม่วาดถนน/รถไฟแบบเดา หรือวาง station label จากความจำ
- ใช้ north, scale และ analytical circle เป็น context ขั้นต่ำ
- overview ใช้สเกลกิโลเมตรต่อพิกเซลเดียวกันทั้งแกนเหนือ–ใต้และตะวันออก–ตะวันตก ไม่ยืดรูปเพื่อให้เต็มกรอบ
- แสดง landmark ไม่เกิน 1–3 จุดเฉพาะเมื่อมี source ที่ยืนยันตัวตนและพิกัดได้ และช่วยตัดสินใจจริง
- ไม่มี sample restaurant dots
- ไม่มี decorative POI
- ไม่ให้ map ทำหน้าที่แทน evidence table

### 10.3 Competitor marker

marker ทุกจุดต้อง:

- มี `competitor_id` คงที่
- ผูกกับ source URL และ coordinate confidence
- มี hit target โปร่งใสอย่างน้อย 44×44 px
- คลิก แตะ หรือกด Enter บน marker link เพื่อเปิดชื่อ ระยะ impact class size basis status และ source
- กด Escape เพื่อปิดรายละเอียดที่เปิดจาก marker และคืน focus ไปยัง marker เดิม
- มี non-map table fallback ครบ
- มีรูปทรงหรือ label นอกเหนือจากสี

ขนาด marker ใช้ตามลำดับ:

1. verified operator leasable area
2. operator project/commercial metric พร้อมชื่อชนิด metric
3. analytical impact class

ห้ามเอา GFA, GLA, project area, shop capacity และ brand count มาอยู่ใน scale เดียวโดยไม่บอกชนิด

### 10.4 Marker ที่ต้อง hold

- **Market Place Pracha Uthit:** host centroid ยังใช้ tenant-in-mall proxy
- **Esplanade Ratchada:** host centroid ยังใช้ tenant-branch proxy

ทั้งสอง venue ยังคงอยู่ใน competitor evidence/table และ diagnostic ตาม registry แต่ไม่ควร plot จนกว่าจะปิด coordinate gate

### 10.5 Map manifest ขั้นต่ำ

ต้องลงทะเบียน:

- candidate IDs 10 แห่ง
- overview map 1 ชุด
- detail map 1 ชุดต่อ candidate
- analytical catchment geometry ที่ใช้ให้คะแนน
- candidate center lineage
- competitor point/source/confidence/render status
- marker size basis
- omitted roads/rail policy
- accessible summary และ table fallback

---

## 11. UX/UI design — Release 1.6

### 11.1 Design objective

หน้ารายงานต้องช่วยผู้บริหารตอบสามคำถามตามลำดับ:

1. ทำเลใดยังน่าสนใจหลังดูคู่แข่ง
2. คู่แข่งรายใดเปลี่ยนคำตัดสิน และเพราะอะไร
3. ต้องตรวจอะไรต่อก่อนเปิด parcel work

ลำดับ presentation:

1. decision strip
2. canonical ranking
3. competition action tiers
4. overview
5. candidate cards + competitor map/table
6. 80/20 illustrative scenario
7. method/limitations
8. source register

### 11.2 J Lifestyle Center Design System v0.3

ใช้ `data-brand="parc"` และรักษา composition:

- Canvas/Alt/Card 65–75%
- Garden + official PARC identity 20–30%
- Bougainvillea ไม่เกิน 5%
- motif ระดับ Q0–Q1 สำหรับ data/report surfaces

หลักสำคัญ:

- useful information → clear invitation → human warmth → brand flourish
- quiet does not mean faint
- ใช้ whitespace, rhythm และ hierarchy สร้างความสงบ
- ไม่ใช้ nested cards หรือ pill มากเกินจำเป็น
- ใช้ border/spacing ก่อน shadow
- mobile stacking ถูกออกแบบโดยตั้งใจ

### 11.3 Typography

| Role | Release 1.6 |
|---|---|
| Heading | Anuphan 300; Thai tracking = 0 |
| Body/reading | IBM Plex Sans Thai Looped 400, ≥18 px, line-height 1.65–1.8 |
| UI/control/data label | IBM Plex Sans Thai Looped 500, ≥16 px |
| Metadata | IBM Plex Sans Thai Looped 400, ≥14 px และไม่ใช้กับข้อมูล critical |
| Numeral/data | IBM Plex 400/500 + tabular numerals |

Anuphan 100 ไม่ใช้กับ controls, table, charts, metrics หรือข้อความ operational

### 11.4 Colour and contrast

- light canvas: `#F7F2E9`; primary ink `#24312F`
- Garden surface: `#365E55`; primary text white
- PARC primary action: Garden + white
- outline controls: `border.control #85776C`
- focus: 3 px `#A94372` + offset 3 px บน light; white/garden approved pair บน dark
- normal text ≥4.5:1; sustained reading ตั้งเป้า ≥7:1
- meaningful boundary/focus/chart mark ≥3:1
- ห้ามใช้ opacity ทำให้ข้อความดู muted

### 11.5 Transparent adaptive logo

Release 1.6 ใช้โลโก้พื้นโปร่งใสเสมอ:

- positive green artwork บน Canvas/Card/พื้นสว่าง
- reverse white artwork บน Garden/Ink/พื้นมืด
- switch ตาม rendered surface/theme ไม่ใช่เติมกล่องขาวหลังโลโก้
- ตรวจ contrast กับพื้นจริงทุก state

**Governance note:** Design System v0.3 ระบุให้รักษา official artwork และไม่ recolor โลโก้ตามใจ การใช้ reverse derivative ใน Release 1.6 เป็นข้อยกเว้นตามคำสั่งโดยตรงสำหรับ contrast โดยต้องรักษา geometry และ alpha เดิม ไม่ใช้สี logo เป็น semantic status และควรแทนด้วย official reverse master เมื่อได้รับไฟล์จากเจ้าของแบรนด์

ภาพดอกเฟื่องฟ้าและผีเสื้อที่แนบมาใช้เป็น reference เท่านั้น ไม่เผยแพร่ ไม่ trace และไม่ใช้ภาพที่มี watermark

### 11.6 Single theme-cycle control

รวม System / Light / Dark เป็นปุ่มเดียว ค่าเริ่มต้นตามอุปกรณ์

ลำดับเมื่อกด:

1. System
2. explicit theme ที่ตรงข้ามกับผลของ System ขณะนั้น
3. explicit theme ฝั่งตรงข้ามกับข้อ 2
4. กลับ System

ตัวอย่าง:

- อุปกรณ์อยู่ Light: `System → Dark → Light → System`
- อุปกรณ์อยู่ Dark: `System → Light → Dark → System`

ข้อกำหนด:

- icon แสดง **สถานะปัจจุบัน**: monitor/system, sun/light, moon/dark
- `aria-label` และ `title` บอกสถานะปัจจุบันและการกดครั้งถัดไป
- มี `aria-live="polite"` สำหรับประกาศการเปลี่ยน theme
- System mode ต้องฟัง `prefers-color-scheme` ที่เปลี่ยนระหว่าง session
- บันทึก explicit preference; การกลับ System ต้องล้าง explicit override
- target ขั้นต่ำ 44×44 px; เป้าหมาย 48×48 px
- control เป็น quiet outline/transparent treatment; hover/focus/pressed ชัดแต่ไม่ดัง
- ไม่ใช้ `aria-pressed` เพราะไม่ใช่ binary state

### 11.7 Clean and quiet controls

controls ที่มี behavior คล้ายกันใช้ pattern เดียว:

- หนึ่ง action ต่อหนึ่ง control
- icon 20–24 px + concise accessible label
- border/spacing สร้างขอบเขต ไม่ใช้ shadow ถ้าไม่มี elevation จริง
- selected/open state มี icon/chevron/label ร่วมกับสี
- touch target ≥44 px
- focus visible
- motion สั้นและมีความหมาย; `prefers-reduced-motion` ปิด transition ที่ไม่จำเป็น

### 11.8 Candidate and evidence components

| Component | Contract |
|---|---|
| Candidate header | canonical rank + name + baseline score |
| Competition strip | verified count + pressure + room + readiness + action tier |
| Decision caveat | decision-changing caveat อยู่ inline ไม่ซ่อน |
| Map | analytical circle + verified competitor markers; ไม่มีถนน/rail ที่ไม่ยืนยัน |
| Competitor marker | size basis เปิดเผย; keyboard/touch accessible |
| Competitor details | name, distance, impact, metric type, source, confidence |
| Evidence disclosure | full-width CTA; “เปิดหลักฐาน/ซ่อนหลักฐาน”; icon + chevron |
| Scenario | ป้ายชัดว่า “Illustrative 80/20 — ไม่ใช่อันดับหลัก” |
| Fallback | competitor table และคำอธิบายครบเมื่อ JS หรือ map ใช้ไม่ได้ |

### 11.9 Responsive behavior

- 320–479 px: single column, full-width evidence CTA, map/table stack, ไม่มี horizontal overflow
- 480–767 px: single column พร้อม metric summary แบบ 2 แถว
- 768–1023 px: comparison grid 2 columns ตามพื้นที่จริง
- ≥1024 px: reading column และ evidence panel แยกกัน แต่ body text ไม่กว้างเกิน 38–42 rem
- table ที่กว้างใช้ semantic stacked rows บน mobile ไม่บังคับ pinch/side scroll สำหรับข้อมูลหลัก

---

## 12. Accessibility contract

- heading order มี H1 เดียวและไม่ข้ามระดับ
- controls ใช้ native button/details/summary เท่าที่ทำได้
- marker และ filter ใช้ได้ด้วย keyboard
- visible focus 3 px
- touch target ≥44×44 px
- selected/open/current state ไม่พึ่งสีอย่างเดียว
- map มี concise text alternative และ table fallback
- tooltip/popover ปิดด้วย Escape และคืน focus
- `aria-live` ใช้กับจำนวนผล filter และ theme status
- zoom 200% ไม่มี clipping, overlap หรือ content loss
- reduced-motion support
- print view ไม่พิมพ์ controls ที่ไร้ความหมาย แต่คง caveat, table และ sources
- core reading task ยังทำงานเมื่อ JavaScript ปิด

---

## 13. QA และ release gates

### 13.1 Analysis checks ที่มีหลักฐานแล้ว

- [x] คง Release 1.5 canonical rank
- [x] ทุก candidate ใช้ Locale Insight release เดียวกัน
- [x] ทุก candidate ใช้ catchment rule และพื้นที่เดียวกัน
- [x] แยก baseline score ออกจาก competition diagnostic
- [x] deduplicate ICONSIAM–ICS และ Siam Piwat Siam clusters
- [x] scoring outputs ไม่มี warning และไม่มี exclusion
- [x] 80/20 ระบุเป็น illustrative noncanonical
- [x] competitor weakness ทุกข้อเป็น hypothesis
- [x] ไม่ใช้ proxy GLA/tenant count เป็น reported fact

### 13.2 Data gates ที่ยังเปิด

- [ ] completeness-certified competitor census ทุก catchment
- [ ] Market Place Pracha Uthit host centroid
- [ ] Esplanade Ratchada host centroid
- [ ] สำเหร่ source polygon/parcel และ candidate recenter
- [ ] วังหลัง/บ้านแขก river-network catchment
- [ ] ราชเทวี/ดินแดง dense-cluster completeness
- [ ] field evidence สำหรับ vacancy, occupancy, traffic, service หรือ tenant weakness หากจะอ้าง

### 13.3 HTML pre-publish QA

- [x] report payload, map manifest และ HTML candidate IDs ตรงกัน
- [x] rank/score/action tier/competitor count ตรงกับ JSON
- [x] one overview + ten detail maps
- [x] roads/rail/stations ที่ไม่มี lineage เป็นศูนย์
- [x] held markers ไม่ถูก plot
- [x] marker size basis และ source เปิดได้
- [x] map/table fallback ครบ
- [x] transparent positive/reverse logo สลับถูกต้อง
- [x] theme cycle ผ่านทั้ง OS-light และ OS-dark sequence
- [x] System mode ตอบสนองต่อ OS theme change
- [x] mobile 320, 375, 768, 1024 และ 1440 px
- [x] keyboard, focus, Escape, focus return
- [x] Light, Dark, System
- [x] 200% text zoom, print, reduced motion
- [x] ไม่มี horizontal overflow หรือ console error
- [x] font weights โหลดจริง
- [x] contrast และ control boundary ผ่านเกณฑ์

### 13.4 Post-publish QA

- [ ] Production เสิร์ฟ revision ที่อนุมัติ
- [ ] HTML byte/hash ตรงกับ release artifact
- [ ] assets/logo/JSON/map manifest โหลดครบ
- [ ] interaction smoke test บน Production
- [ ] canonical rank, 80/20 label และ data disclosure ตรงกับ source
- [ ] public source links เปิดได้

**Release rule:** ยังไม่ประกาศ `PASS` จนกว่าจะตรวจหน้า rendered จริงก่อนและหลังเผยแพร่

---

## 14. Risk register

| Risk | ระดับ | ผลต่อการตัดสิน | วิธีปิด |
|---|---|---|---|
| Competitor registry เป็น minimum set | Decision-changing | room อาจสูงเกินจริง | complete census + entity resolution |
| Straight-line catchment ข้ามแม่น้ำ/โครงข่าย | Decision-changing | overlap อาจสูงหรือต่ำผิด | network/travel-time model |
| Candidate center ไม่ใช่ parcel | Decision-changing | สำเหร่เกือบตรง incumbent | source polygon + recenter |
| Strategic gap เป็น heuristic | Material | 80/20 rank ไวต่อ weight | field evidence + recalibration |
| Missing vs zero ใน baseline | Material | candidate coverage บางอาจถูกกดคะแนน | rerun missing-data policy |
| GLA/tenant proxy | Material | marker size และ impact อาจดูแม่นเกินจริง | operator metric or disclosed class |
| Dense cluster double count | Material | pressure สูงเกินจริง | parent-cluster dedup; review ownership/precinct |
| Competitor weakness inferred without evidence | P0 claim risk | strategy ผิดและความน่าเชื่อถือลด | claim firewall + field audit |
| Roads/rail shown inaccurately | P0 trust risk | map ทำให้รายงานไม่น่าเชื่อถือ | omit until feature lineage verified |
| Adaptive logo not official reverse master | Brand governance | ขัด artwork policy | explicit exception + obtain official reverse asset |
| Scenario read as final rank | Decision-changing | ย้าย priority ก่อน evidence พร้อม | persistent noncanonical label |

---

## 15. Source register

### 15.1 Internal/source artifacts

1. `Project brief - PARC Bangna(1).md`
2. `J_Lifestyle_Center_Design_System_v0.3.md`
3. `PARC_Bangna_Bangkok_Top_10_Release_1_5_Analysis_and_UXUI_2026-07-27.md`
4. `venue_locale_fundamental_data_audit_v0_1_2026-07-27.md`
5. `analysis/concept-contract.json`
6. `analysis/competitor-registry.public.json`
7. `analysis/competitor-score-breakdown.json`
8. `analysis/screening-results.json`
9. `analysis/competition-scenario-results.json`
10. [Release 1.5 immutable source](https://github.com/montri-th/top10locations-like-parcbn/blob/563146f6b8f57d25652cea9f60acb6ee9239a054/index.html)

### 15.2 Competitor operating/status and metric sources

- Platform Wongwian Yai: [official Facebook](https://www.facebook.com/platform.wongwianyai/?locale=th_TH), [Bangkok Metropolitan Administration](https://webportal.bangkok.go.th/VPH/page/main/7144/Activities/0/info/52517)
- ICONSIAM: [official directory](https://www.iconsiam.com/en/directory), [Siam Piwat project context](https://www.siampiwat.com/en/news-detail.php?id=6)
- ICS Lifestyle Complex: [official site](https://ics.iconsiam.com/)
- SENA Fest: [official project page](https://www.senafest.com/en/about)
- The Mall Lifestore Tha Phra: [official branch page](https://themalllifestore.com/branch/thapra), [official directory](https://themalllifestore.com/directory)
- KINGSQUARE Community Mall: [official site](https://kingsquaremall.com/), [Bangkok Post opening report](https://www.bangkokpost.com/business/general/3094336/mall-opens-doors-at-kingsquare-project)
- Terminal21 Rama 3: [official site](https://www.terminal21.co.th/rama3/en/home-en/), [official directory](https://www.terminal21.co.th/rama3/en/shop-categories-en/home-en2/)
- Central Rama 3: [official property page](https://www.centralpattana.co.th/en/our-business/shopping-center/8/central-rama-3)
- Riverside Plaza Bangkok: [official site](https://www.riverside-plaza.com/), [official directory](https://www.riverside-plaza.com/directory/)
- The Old Siam Plaza: [official site](https://theoldsiam.co.th/en/)
- Tha Maharaj: [official Facebook information](https://www.facebook.com/ThaMaharaj/about/), [Time Out Bangkok](https://www.timeout.com/bangkok/shopping/tha-maharaj)
- Central Pinklao: [official property page](https://www.centralpattana.co.th/en/our-business/shopping-center/7/central-pinklao)
- Market Place Pracha Uthit: [Central Pattana project announcement](https://www.centralpattana.co.th/en/shopping/shopping-update/lifestyle-activities/1530/central-pattana-unveils-market-place-pracha-uthit-anchoring-a-high-potential-location-with-a-neighborhood-centric-strategy-to-create-the-best-community-mall-in-the-area), [official Facebook](https://www.facebook.com/marketplaceprachauthit/)
- Siam Discovery: [official site](https://www.siamdiscovery.co.th/)
- Siam Center: [official site](https://www.siamcenter.co.th/), [official directory](https://www.siamcenter.co.th/directory)
- Siam Paragon: [official directory](https://www.siamparagon.co.th/directory)
- Platinum Fashion Mall: [official directory](https://platinumfashionmall.com/directory/)
- centralWorld: [official property page](https://www.centralpattana.co.th/en/our-business/shopping-center/9/centralworld)
- MBK Center: [official site](https://www.mbk-center.co.th/en/)
- Fortune Town: [official site](https://fortunetown.co.th/en/contact-us/), [official directory](https://fortunetown.co.th/shops/)
- Central Rama 9: [official branch page](https://shoppingcenter.centralpattana.co.th/branch/central-rama-9/branch-information/)
- Esplanade Ratchada: [Central Pattana 2026 operating activity](https://www.centralpattana.co.th/en/shopping/shopping-update/event/1577/grand-grand-sale-2026)
- The Street Ratchada: [official Facebook](https://www.facebook.com/TheStreetRatchada/), [official Instagram](https://www.instagram.com/thestreetratchada/)
- Central Pattana comparable asset metrics: [Retail Properties](https://www.centralpattana.co.th/en/investor-relations/assets-under-central-pattana/retail-properties)

### 15.3 Source handling notes

- operator metric dates and definitions are preserved in `competitor-registry.public.json`
- forecast is labeled forecast
- historical project metric is not presented as current GLA
- social pages support operating/current activity only where declared
- coordinate sources and confidence are separate from operating-status sources

---

## 16. Final recommendation

Release 1.6 ควรรักษา **canonical Top 10 ของ Release 1.5** เพื่อให้ lineage และ comparable basis ไม่ขาด แต่เปลี่ยนวิธีใช้ผลดังนี้:

1. อย่าใช้วงเวียนใหญ่–ตะวันออกหรือเจริญราษฎร์เป็น default Wave 1 โดยไม่ผ่าน competition gate
2. ยกบางปะกอกเป็น field-priority case เพราะเป็นสมดุลที่ดีที่สุดในรอบนี้ระหว่าง baseline, competitive room และ evidence readiness
3. หยุดสำเหร่จนกว่าจะยืนยัน center/parcel
4. อย่าเลื่อนวังหลังหรือประชาอุทิศจาก scenario 80/20 จนกว่าจะปิด river/centroid/completeness gaps
5. ลด priority ราชเทวีและดินแดง เว้นแต่มี micro-format หรือ parcel advantage ที่เปลี่ยนโจทย์
6. เก็บ “จุดอ่อนคู่แข่ง” เป็น hypothesis และออกแบบ fieldwork ให้พิสูจน์ ไม่เขียนเป็น fact
7. ให้แผนที่แสดงเฉพาะ analytical geometry และ competitor POI ที่ตรวจ lineage ได้; ตัดถนน/rail/station ที่ไม่มั่นใจออก
8. รักษาภาษาและ information architecture ของ 1.5 แต่เพิ่ม competition strip, action tier, clickable competitor evidence และ noncanonical label ที่ชัด
9. ใช้ transparent adaptive logo, single theme-cycle control และ clean/quiet interaction ตามข้อกำหนดในเอกสารนี้
10. เผยแพร่เมื่อ payload, map manifest, HTML และ rendered QA ตรงกันเท่านั้น

> **Decision CTA:** อนุมัติ Release 1.6 field-validation plan โดยเริ่มจากบางปะกอก และทำ competition-first gate ที่วงเวียนใหญ่–ตะวันออกกับเจริญราษฎร์ พร้อมปิด geometry/evidence gaps ก่อนเปลี่ยนอันดับหลัก
