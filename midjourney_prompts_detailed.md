# V3 알고리즘 시각화 - 상세 Midjourney 프롬프트

## 전체 개요

V3 밴드 추천 알고리즘을 8개 장면으로 구성하여 시각화합니다. 각 프롬프트는 기술적 다이어그램 스타일, 미니멀 흑백 색상으로 통일되며, 3D 벡터 공간에서의 수학적 변환 과정을 표현합니다.

---

## Scene 1: 초기 상태 - 밴드 벡터들의 분산

### 목적
사용자가 선택한 10-15개 밴드를 3D 공간의 벡터(화살표)로 표현. 각 벡터는 다른 방향을 향하며 산재되어 있음.

### Midjourney 프롬프트
```
3D coordinate system with XYZ axes labeled, 12-15 vector arrows scattered in different directions, each arrow originates from origin point, arrows in varying shades of gray (light to dark gradient), clean white background, subtle grid plane at base, isometric camera angle 45 degrees, technical blueprint style, mathematical precision, arrows have cylindrical shafts and conical heads, minimal shadows, scientific data visualization, geometric accuracy, depth perception through size variation, professional technical illustration --ar 16:9 --style raw --v 6
```

### 세부 설명
- **좌표계**: X, Y, Z 축이 명확하게 표시된 3차원 좌표계
- **벡터 표현**: 원점에서 시작하는 12-15개의 화살표
- **색상**: 밝은 회색에서 어두운 회색으로 그라데이션
- **배경**: 깨끗한 흰색 배경, 바닥에 미세한 그리드
- **카메라**: 45도 각도의 등각 투영
- **디테일**: 화살표는 원통형 몸체와 원뿔형 머리를 가짐

---

## Scene 2: K-means 클러스터링 시작

### 목적
벡터들이 3개 그룹으로 분류되기 시작하는 과정. 각 벡터에서 미래의 클러스터 중심으로 가는 가느다란 점선 표시.

### Midjourney 프롬프트
```
3D space with 12-15 vector arrows beginning to organize into three groups, thin dotted lines connecting each arrow to three emerging cluster centers, cluster centers shown as small transparent spheres, minimal monochrome palette with three distinct gray tones (light gray, medium gray, dark gray) for three groups, vectors starting to lean toward their respective centers, mathematical clustering visualization, isometric view, clean geometry, technical diagram aesthetic, motion implied through positioning, scientific precision, depth through layering --ar 16:9 --style raw --v 6
```

### 세부 설명
- **연결선**: 각 벡터에서 가장 가까운 클러스터 중심으로 향하는 점선
- **클러스터 중심**: 3개의 작고 투명한 구체로 표시
- **그룹화**: 벡터들이 3가지 회색 톤으로 구분되기 시작
- **움직임 표현**: 벡터들의 위치와 기울기로 클러스터링 진행 중임을 암시
- **수학적 시각화**: K-means의 반복적 할당 과정을 시각적으로 표현

---

## Scene 3: 클러스터링 완료

### 목적
명확하게 3개 그룹으로 구분된 최종 클러스터 상태. 같은 그룹 내 벡터들은 서로 가깝게 위치.

### Midjourney 프롬프트
```
3D coordinate space with vectors clearly separated into three distinct clusters, cluster A in light gray (5 vectors), cluster B in medium gray (4 vectors), cluster C in dark gray (5 vectors), vectors within same cluster positioned closer together with 15-20 degree angular separation, clear spatial gaps between different clusters, minimal technical diagram, precise geometric arrangement, each cluster occupies distinct region of 3D space, clean separation visible from isometric angle, mathematical clustering result, scientific visualization, professional technical illustration, depth and dimension clearly defined --ar 16:9 --style raw --v 6
```

### 세부 설명
- **3개 클러스터**: 
  - 클러스터 A (밝은 회색): 5개 벡터
  - 클러스터 B (중간 회색): 4개 벡터
  - 클러스터 C (어두운 회색): 5개 벡터
- **공간 배치**: 각 클러스터는 3D 공간의 서로 다른 영역 차지
- **각도 분리**: 같은 클러스터 내 벡터는 15-20도 간격
- **명확한 구분**: 클러스터 간 공간적 간격이 뚜렷함

---

## Scene 4: Centroid 생성

### 목적
각 클러스터의 중심점(centroid)을 큰 구체로 표시. Centroid는 해당 클러스터 벡터들의 평균 방향을 나타냄.

### Midjourney 프롬프트
```
3D vector space with three distinct clusters, each cluster has a large sphere at geometric center representing centroid, centroids are 3x larger than vector arrow heads, centroids in solid black with subtle radial glow effect, smaller vector arrows surround each centroid in matching gray shade, centroid position calculated as weighted average of cluster members, technical diagram with mathematical precision, isometric perspective, clean minimal design, centroids labeled internally with subtle texture, scientific visualization showing statistical center of mass, professional technical illustration, clear hierarchy between centroids and vectors --ar 16:9 --style raw --v 6
```

### 세부 설명
- **Centroid 크기**: 벡터 화살촉보다 3배 크게 표현
- **시각적 강조**: 검은색 구체 + 미세한 방사형 글로우
- **위치**: 각 클러스터의 기하학적 중심 (가중 평균 위치)
- **계층 구조**: Centroid가 벡터들보다 시각적으로 우세하게 표현
- **수학적 의미**: 통계적 질량 중심을 나타냄
- **3개 Centroid**: 각각 밝은, 중간, 어두운 회색 클러스터의 중심

---

## Scene 5: 키워드 벡터 등장

### 목적
새로운 키워드 벡터가 3D 공간에 극적으로 등장. 기존 클러스터들과 다른 방향에서 나타남.

### Midjourney 프롬프트
```
3D coordinate space with three cluster centroids as black spheres in light, medium, dark gray clusters, a new prominent vector arrow entering from upper right quadrant, keyword vector is thicker (2x standard width) and in deepest black color with subtle highlight, keyword vector originates from origin and points in unique direction different from all clusters, dramatic entrance emphasized by faint motion lines or glow trail, keyword vector clearly distinguished by size and darkness, minimal monochrome technical diagram, isometric view, clean geometric composition, new element introduction with visual impact, mathematical precision, scientific visualization showing external influence vector --ar 16:9 --style raw --v 6
```

### 세부 설명
- **키워드 벡터 특징**:
  - 두께: 일반 벡터의 2배
  - 색상: 가장 어두운 검은색
  - 미세한 하이라이트로 강조
- **방향**: 기존 모든 클러스터와 다른 독특한 방향
- **등장 연출**: 
  - 오른쪽 위 사분면에서 등장
  - 희미한 모션 라인 또는 글로우 트레일
- **시각적 구분**: 크기와 색상으로 명확하게 구별
- **의미**: 외부 영향 벡터 (사용자가 입력한 키워드)

---

## Scene 6: Slerp 경로 표시

### 목적
각 centroid가 키워드 벡터 방향으로 구면을 따라 회전할 경로를 곡선으로 표시. Slerp(Spherical Linear Interpolation)의 핵심 개념 시각화.

### Midjourney 프롬프트
```
3D coordinate system with three centroids as black spheres, keyword vector in deep black, curved arc paths drawn from each centroid toward keyword vector, arcs follow surface of invisible sphere centered at origin, paths shown as dotted curves with 20-30 dots per curve, each arc represents spherical linear interpolation trajectory, transparent sphere outline (radius equals vector length) shown with faint dashed line to indicate spherical surface, mathematical elegance of great circle paths, three different arc lengths showing varying degrees of rotation needed, isometric technical diagram, minimal monochrome style, geometric precision showing spherical geometry, scientific visualization of SLERP interpolation, angle theta marked between original and target directions --ar 16:9 --style raw --v 6
```

### 세부 설명
- **Slerp 경로**:
  - 3개의 곡선 아크, 각 centroid에서 키워드 방향으로
  - 원점을 중심으로 한 구면의 표면을 따라감
  - 점선으로 표시 (곡선당 20-30개 점)
- **구면 표시**: 
  - 투명한 구 외곽선 (반지름 = 벡터 길이)
  - 희미한 점선으로 표시
  - 구면 기하학을 명확하게 보여줌
- **수학적 표현**:
  - 대원(great circle) 경로
  - 3개의 서로 다른 아크 길이 (필요한 회전 각도가 다름)
  - 원본 방향과 목표 방향 사이의 각도 θ 표시
- **핵심 개념**: 직선이 아닌 구면을 따라 보간됨을 시각화

---

## Scene 7: Slerp 적용 후

### 목적
Centroid들이 키워드 방향으로 회전한 최종 위치. 원래 위치는 유령 같은 아웃라인으로, 새 위치는 실선으로 표시하여 변화를 명확히 보여줌.

### Midjourney 프롬프트
```
3D vector space showing transformation result, three adjusted centroids in new positions rotated toward keyword vector, original centroid positions shown as transparent ghost outlines (30% opacity) in light gray, new centroid positions as solid black spheres, curved rotation arrows (ribbon-style) connecting old to new positions along spherical paths, each rotation arrow shows direction and magnitude of movement, angular displacement labeled (15-25 degrees per centroid), keyword vector remains in deep black as reference point, clear before-after comparison in single frame, minimal monochrome technical diagram, isometric view, mathematical precision showing spherical rotation transformation, clean geometric visualization of vector space manipulation, scientific illustration of adaptive interpolation result --ar 16:9 --style raw --v 6
```

### 세부 설명
- **원래 위치 (Before)**:
  - 투명한 유령 아웃라인 (30% 불투명도)
  - 밝은 회색으로 표시
  - 희미하게 보여서 "이전" 상태임을 표시
- **새 위치 (After)**:
  - 실선 검은색 구체
  - 키워드 방향으로 회전된 위치
  - 명확하고 강하게 표시
- **회전 표시**:
  - 리본 스타일의 곡선 화살표
  - 구면 경로를 따라 이전 → 새 위치 연결
  - 이동 방향과 크기를 보여줌
- **각도 정보**:
  - 각 centroid의 각변위 표시 (15-25도)
  - Adaptive t의 결과를 수치로 표현
- **키워드 벡터**: 기준점으로 깊은 검은색 유지
- **비교 효과**: 단일 프레임에서 변화 전후를 동시에 보여줌

---

## Scene 8: 최종 추천 결과

### 목적
각 조정된 centroid에서 가장 가까운 밴드 벡터 1개씩 선택. 선택된 3개 밴드를 시각적으로 강조하여 최종 추천 결과 표시.

### Midjourney 프롬프트
```
3D vector space with three adjusted centroids highlighted as large black spheres with bright halos, all original band vectors shown in light gray (backgrounded), three selected recommendation vectors emphasized with thick arrows (2.5x normal width) in darkest black, glowing connection lines from each centroid to its nearest selected band, connection lines shown as straight solid lines with gradient fade, selected bands have circular highlight rings at arrow tips, visual hierarchy clear: centroids largest, selected bands prominent, other vectors faded, minimal monochrome technical diagram, isometric perspective, clean winner indication through size and darkness, scientific visualization of final recommendation algorithm output, professional technical illustration showing optimization result, clear visual distinction between selected and non-selected elements --ar 16:9 --style raw --v 6
```

### 세부 설명
- **조정된 Centroid**:
  - 큰 검은색 구체
  - 밝은 헤일로(후광) 효과로 강조
  - 시각적 계층의 최상위
- **원본 밴드 벡터들**:
  - 밝은 회색으로 배경화
  - 희미하게 표시되어 선택되지 않음을 나타냄
- **선택된 3개 밴드**:
  - 두꺼운 화살표 (일반의 2.5배)
  - 가장 어두운 검은색
  - 화살촉 끝에 원형 강조 링
- **연결선**:
  - 각 centroid에서 선택된 밴드로 직선
  - 실선, 그라데이션 페이드 효과
  - 가장 가까운 관계를 시각적으로 표현
- **시각적 계층**:
  1. Centroid (가장 크고 강조됨)
  2. 선택된 밴드 (굵고 어두움)
  3. 비선택 밴드 (희미함)
- **알고리즘 결과**: 최적화된 추천 결과를 명확하게 시각화

---

## 일관성 유지를 위한 공통 파라미터

### 필수 파라미터
```
--ar 16:9        # 16:9 비율
--style raw      # 기술적/다이어그램 스타일 강조
--v 6            # Midjourney 버전 6
```

### 권장 추가 파라미터
```
--seed [고정숫자]  # 스타일 일관성 유지 (예: --seed 12345)
--stylize 50      # 기술적 정확성 우선 (낮은 stylize 값)
--chaos 0         # 일관된 출력 (변동성 최소화)
```

### 프롬프트 공통 키워드
- `isometric view` / `isometric perspective` - 등각 투영
- `minimal monochrome` - 미니멀 흑백
- `technical diagram` - 기술 다이어그램
- `scientific visualization` - 과학적 시각화
- `mathematical precision` - 수학적 정밀도
- `clean geometry` - 깨끗한 기하학
- `professional technical illustration` - 전문 기술 일러스트레이션

---

## 영상 제작 워크플로우

### 1단계: Midjourney에서 이미지 생성
1. Scene 1 프롬프트 입력 → 마음에 드는 결과 선택
2. 해당 이미지의 `--seed` 값 확인 (이미지 우클릭 → Copy Seed)
3. Scene 2-8 프롬프트에 동일한 `--seed` 추가하여 생성
4. 각 장면마다 4개 변형 중 가장 일관된 것 선택
5. Upscale (U1-U4) 실행하여 고해상도 이미지 저장

### 2단계: 후처리 (선택사항)
- **Photoshop / Figma**:
  - 텍스트 레이블 추가: "Cluster 1", "Cluster 2", "Cluster 3"
  - "Keyword Vector", "Centroid", "SLERP" 등의 설명 텍스트
  - 화살표나 주석 추가
- **색상 조정**:
  - 일관된 흑백 톤 유지
  - 대비 조정으로 가독성 향상

### 3단계: 영상 편집 (After Effects / Premiere / DaVinci Resolve)
```
타임라인 구성:
Scene 1: 0:00 - 0:02 (2초)
Scene 2: 0:02 - 0:04 (2초)
Scene 3: 0:04 - 0:06 (2초)
Scene 4: 0:06 - 0:09 (3초) - Centroid 개념 설명 중요
Scene 5: 0:09 - 0:11 (2초)
Scene 6: 0:11 - 0:14 (3초) - Slerp 경로 설명 중요
Scene 7: 0:14 - 0:17 (3초) - 변화 비교 시간 필요
Scene 8: 0:17 - 0:20 (3초) - 최종 결과 강조

전체 길이: 20초
```

### 전환 효과
- **Cross Dissolve**: 0.3초 (부드러운 전환)
- **Fade to Black**: Scene 4→5, Scene 6→7 (새로운 요소 등장 시)

### 애니메이션 추가 (선택사항)
- **Scene 1**: 벡터들이 하나씩 나타나는 효과
- **Scene 2-3**: 클러스터링 진행 애니메이션
- **Scene 5**: 키워드 벡터가 날아오는 모션
- **Scene 6**: 경로를 따라 점선이 그려지는 효과
- **Scene 7**: Centroid가 회전하는 모션
- **Scene 8**: 선택된 밴드가 강조되는 펄스 효과

### 자막/설명 텍스트 (선택사항)
```
Scene 1: "사용자가 선택한 밴드들"
Scene 2-3: "K-means 클러스터링 (k=3)"
Scene 4: "각 클러스터의 중심점 (Centroid)"
Scene 5: "사용자 입력 키워드"
Scene 6: "구면 선형 보간 (SLERP) 경로"
Scene 7: "키워드 방향으로 회전"
Scene 8: "클러스터별 최종 추천 밴드"
```

### 배경음악 추천
- **스타일**: Minimal Techno, Ambient, Electronic
- **BPM**: 80-100 (차분하지만 리듬감 있는)
- **무료 음원 출처**:
  - Epidemic Sound (구독 필요)
  - Artlist (구독 필요)
  - YouTube Audio Library (무료)
  - Free Music Archive (무료)
- **검색 키워드**: "minimal techno", "data visualization", "tech ambient"

---

## 추가 최적화 팁

### 더 좋은 결과를 위한 프롬프트 조정

1. **벡터 개수가 너무 많거나 적을 때**:
   - 프롬프트에서 `12-15 vectors` → `8 vectors` 또는 `20 vectors`로 조정
   
2. **클러스터 크기 불균형 시**:
   - `cluster A (5 vectors), cluster B (4 vectors), cluster C (5 vectors)` 부분 수정

3. **색상 대비가 부족할 때**:
   - `high contrast monochrome` 추가
   - `pure black and white` 추가

4. **3D 느낌이 부족할 때**:
   - `strong depth perception` 추가
   - `dramatic perspective` 추가
   - `volumetric lighting` 추가 (미니멀 스타일에서는 주의)

5. **너무 복잡해 보일 때**:
   - `ultra minimal` 추가
   - `simplified geometry` 추가
   - `reduce visual noise` 추가

### Midjourney 특정 기능 활용

- **Vary (Region)**: 특정 부분만 수정 (예: 벡터 개수만 변경)
- **Remix**: 프롬프트 일부만 변경하여 재생성
- **Zoom Out**: 더 넓은 공간 표현 필요 시
- **Pan**: 카메라 각도 조정 필요 시

### 문제 해결

**문제**: 화살표가 명확하게 나오지 않음
**해결**: `vector arrows with clear cylindrical shafts and conical heads` 추가

**문제**: 구체(centroid)가 너무 작게 표현됨
**해결**: `large prominent spheres, 3x size of arrow heads` 명시

**문제**: 점선 경로가 직선으로 나옴
**해결**: `smooth curved arc paths, NOT straight lines` 강조

**문제**: 색상이 너무 다양하게 나옴
**해결**: `strict monochrome palette, grayscale only` 명시

---

## 최종 체크리스트

영상 제작 전 확인사항:

- [ ] 8개 장면 모두 동일한 `--seed` 값 사용
- [ ] 모든 이미지가 16:9 비율로 생성됨
- [ ] 카메라 각도(isometric)가 일관됨
- [ ] 색상 톤(monochrome)이 통일됨
- [ ] 각 장면의 핵심 요소가 명확히 보임
- [ ] 고해상도 Upscale 완료
- [ ] 필요한 텍스트 레이블 추가 완료
- [ ] 영상 편집 소프트웨어 준비 완료
- [ ] 배경음악 선택 완료
- [ ] 전환 효과 스타일 결정 완료

---

## 마무리

이 프롬프트들은 V3 밴드 추천 알고리즘의 수학적 원리를 시각적으로 명확하게 전달하도록 설계되었습니다. 각 장면은 독립적으로도 이해 가능하지만, 순차적으로 연결될 때 전체 알고리즘의 흐름을 완벽하게 보여줍니다.

**핵심 메시지**:
1. 사용자 취향을 벡터로 표현
2. K-means로 다양한 취향 그룹 분리
3. 각 그룹에 키워드를 구면 보간으로 반영
4. 각 그룹에서 최적의 추천 1개씩 선택

기술적 정확성과 시각적 명확성의 균형을 맞춘 이 프롬프트들로 효과적인 알고리즘 설명 영상을 만드실 수 있을 것입니다.
