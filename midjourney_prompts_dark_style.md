# V3 알고리즘 시각화 - 다크 그리드 스타일 Midjourney 프롬프트

참고 이미지 스타일: 검은 배경 + 3D 그리드 + 벡터(선+구체)

---

## Scene 1: 초기 상태 - 밴드 벡터들의 분산

### 목적
12-15개의 벡터가 3D 공간에 산재되어 있는 상태. 각 벡터는 원점에서 시작하는 흰색 선과 끝점의 구체로 표현.

### Midjourney 프롬프트
```
3D coordinate system on pure black background, subtle grid lines in dark gray forming cube structure, 12-15 vectors as thin white lines originating from center origin, each vector ends with small glowing sphere in different pastel colors (yellow, blue, pink, purple, green), vectors pointing in various directions throughout 3D space, minimal dark aesthetic, clean geometric precision, isometric view at 45 degree angle, mathematical visualization, soft glow on spheres, technical diagram style, depth perception through grid perspective --ar 16:9 --style raw --v 6
```

### 세부 설명
- **배경**: 순수 검은색 (#000000)
- **그리드**: 어두운 회색 선으로 큐브 구조 형성
- **벡터 표현**:
  - 원점에서 출발하는 얇은 흰색 선
  - 끝점에 작은 발광 구체
  - 구체 색상: 파스텔 톤 (노랑, 파랑, 분홍, 보라, 초록) - 12-15개 벡터 구분
- **12-15개 벡터**: 3D 공간 전체에 다양한 방향으로 분산
- **시각 효과**: 구체에 부드러운 글로우 효과
- **카메라**: 45도 등각 투영

---

## Scene 2: K-means 클러스터링 시작

### 목적
벡터들이 3개 그룹으로 분류되기 시작. 같은 그룹의 벡터들은 유사한 색상으로 변하기 시작하고, 미래의 클러스터 중심으로 향하는 희미한 점선 표시.

### Midjourney 프롬프트
```
3D grid cube on black background, 12-15 vectors as white lines with endpoint spheres, spheres beginning to change colors into three groups: group 1 in cyan-blue (4-5 spheres), group 2 in magenta-pink (4-5 spheres), group 3 in yellow-orange (4-5 spheres), thin dotted lines in matching colors connecting spheres to three emerging cluster centers, three small transparent spheres appearing at future centroids, dark minimal aesthetic, clean geometry, mathematical clustering visualization in progress, subtle color transitions, isometric perspective, technical precision --ar 16:9 --style raw --v 6
```

### 세부 설명
- **색상 그룹화 시작**:
  - 그룹 1: 시안-블루 계열 (4-5개 구체)
  - 그룹 2: 마젠타-핑크 계열 (4-5개 구체)
  - 그룹 3: 옐로우-오렌지 계열 (4-5개 구체)
- **클러스터 중심**: 3개의 작고 투명한 구체 등장
- **연결선**: 각 벡터에서 가장 가까운 중심으로 향하는 색상별 점선
- **전환 효과**: 구체 색상이 부드럽게 변화 중
- **배경**: 검은색 + 어두운 회색 그리드 유지

---

## Scene 3: 클러스터링 완료

### 목적
명확하게 3개 그룹으로 구분. 같은 그룹의 벡터들은 공간적으로 가까이 모여있고 동일한 색상.

### Midjourney 프롬프트
```
3D wireframe grid cube on pure black background, vectors clearly separated into three distinct spatial clusters, cluster 1 with 5 cyan-blue glowing spheres grouped in upper-right region, cluster 2 with 4 magenta-pink spheres in lower-left region, cluster 3 with 5 yellow-orange spheres in middle region, white vector lines from origin to each sphere, clear spatial separation between clusters, minimal dark aesthetic, clean geometric arrangement, mathematical clustering complete, vibrant colored spheres with glow against black, isometric view, technical precision, depth through grid perspective --ar 16:9 --style raw --v 6
```

### 세부 설명
- **3개 클러스터 완성**:
  - 클러스터 1: 5개 시안-블루 구체 (우상단 영역)
  - 클러스터 2: 4개 마젠타-핑크 구체 (좌하단 영역)
  - 클러스터 3: 5개 옐로우-오렌지 구체 (중앙 영역)
- **공간 배치**: 각 클러스터가 3D 공간의 서로 다른 영역 차지
- **벡터선**: 모두 흰색 선으로 원점과 연결
- **명확한 구분**: 클러스터 간 공간적 간격
- **시각 효과**: 색상별 구체 글로우 강화

---

## Scene 4: Centroid 생성

### 목적
각 클러스터의 중심에 큰 구체(centroid) 생성. Centroid는 해당 클러스터 색상으로 표시되며 더 밝게 빛남.

### Midjourney 프롬プ트
```
3D grid space on black background, three distinct clusters with small endpoint spheres, three large glowing centroids appearing at geometric center of each cluster: cyan-blue centroid (3x larger, bright glow) for cluster 1, magenta-pink centroid (3x larger, bright glow) for cluster 2, yellow-orange centroid (3x larger, bright glow) for cluster 3, white vector lines from origin to small spheres, centroids significantly brighter and larger than member spheres, dark minimal aesthetic, mathematical precision, centroid as statistical center of mass, isometric perspective, vibrant colors against black void, technical visualization --ar 16:9 --style raw --v 6
```

### 세부 설명
- **Centroid 크기**: 일반 구체보다 3배 크게
- **Centroid 색상 및 효과**:
  - 클러스터 1 centroid: 밝은 시안-블루 + 강한 글로우
  - 클러스터 2 centroid: 밝은 마젠타-핑크 + 강한 글로우
  - 클러스터 3 centroid: 밝은 옐로우-오렌지 + 강한 글로우
- **위치**: 각 클러스터의 기하학적 중심
- **밝기**: Centroid가 멤버 구체보다 훨씬 밝게 빛남
- **벡터선**: 흰색 선은 여전히 원점에서 작은 구체들로 연결
- **계층 구조**: 큰 centroid가 시각적으로 우세

---

## Scene 5: 키워드 벡터 등장

### 목적
새로운 키워드 벡터가 공간에 등장. 흰색 선에 밝은 흰색 또는 무지개색 구체로 표현되어 기존 클러스터들과 구별됨.

### Midjourney 프롬프트
```
3D wireframe grid on black background, three cluster centroids as large glowing spheres in cyan-blue, magenta-pink, yellow-orange, existing member spheres in matching colors with white vector lines, a new prominent keyword vector appearing from upper-right quadrant: thick bright white line (2x normal thickness) from origin, ending with large bright white sphere with rainbow gradient shimmer effect, keyword vector pointing in unique direction different from all clusters, dramatic entrance with motion trail or particle effect, keyword sphere size between normal and centroid size, dark minimal aesthetic, clean geometry, new element clearly distinguished by brightness and effect, isometric view, mathematical precision --ar 16:9 --style raw --v 6
```

### 세부 설명
- **키워드 벡터 특징**:
  - 선: 밝은 흰색, 두께 2배
  - 구체: 밝은 흰색 + 무지개 그라데이션 시머 효과
  - 크기: 일반 구체와 centroid 사이
- **방향**: 기존 모든 클러스터와 다른 독특한 방향
- **등장 연출**: 
  - 우상단에서 등장
  - 모션 트레일 또는 파티클 효과
- **시각적 구분**: 밝기와 효과로 명확하게 구별
- **기존 요소**: 3개 centroid와 멤버 구체들 유지

---

## Scene 6: Slerp 경로 표시

### 목적
각 centroid에서 키워드 벡터 방향으로 구면을 따라 회전할 경로를 곡선 아크로 표시.

### Midjourney 프롬프트
```
3D grid cube on pure black background, three large glowing centroids (cyan-blue, magenta-pink, yellow-orange), bright white keyword vector with shimmer sphere, curved arc paths drawn from each centroid toward keyword vector in matching colors: cyan arc from blue centroid, magenta arc from pink centroid, yellow arc from orange centroid, arcs follow invisible spherical surface centered at origin, paths shown as dotted glowing curves with 25-30 luminous dots per curve, transparent sphere outline with radius equal to vector length shown as faint wireframe, great circle paths on sphere surface, three different arc lengths showing varying rotation angles, dark minimal aesthetic, mathematical elegance of spherical linear interpolation, isometric perspective, vibrant colored arcs glowing against black void --ar 16:9 --style raw --v 6
```

### 세부 설명
- **Slerp 경로 (3개 아크)**:
  - 시안 아크: 블루 centroid → 키워드 방향
  - 마젠타 아크: 핑크 centroid → 키워드 방향
  - 옐로우 아크: 오렌지 centroid → 키워드 방향
- **경로 표현**:
  - 각 아크는 25-30개의 발광 점들로 구성
  - 클러스터 색상과 매칭
  - 구면 표면을 따라가는 곡선
- **구면 표시**: 투명한 구 외곽선 (희미한 와이어프레임)
- **3개의 서로 다른 아크 길이**: 각 centroid마다 필요한 회전 각도가 다름
- **수학적 표현**: 대원(great circle) 경로
- **시각 효과**: 검은 배경에 빛나는 색상 아크

---

## Scene 7: Slerp 적용 후

### 목적
Centroid들이 키워드 방향으로 회전 완료. 원래 위치는 희미한 반투명 구체, 새 위치는 밝은 구체로 표시.

### Midjourney 프롬프트
```
3D wireframe grid on black background, three adjusted centroids in new positions rotated toward keyword vector: bright glowing cyan-blue sphere, bright magenta-pink sphere, bright yellow-orange sphere in new locations, original centroid positions shown as ghost outlines (20% opacity, darker versions) in same colors at original positions, curved ribbon-style rotation arrows in matching colors flowing from old to new positions along spherical paths, rotation arrows with gradient fade and glow effect, keyword vector remains as bright white with shimmer, angular displacement visible (15-25 degrees per centroid), clear before-after comparison in single frame, dark minimal aesthetic, mathematical precision of spherical rotation, vibrant new positions contrasted with dim ghost positions, isometric view --ar 16:9 --style raw --v 6
```

### 세부 설명
- **새 위치 (After)**:
  - 밝게 빛나는 시안-블루 구체
  - 밝게 빛나는 마젠타-핑크 구체
  - 밝게 빛나는 옐로우-오렌지 구체
  - 키워드 방향으로 회전된 새 위치
- **원래 위치 (Before)**:
  - 유령 아웃라인 (20% 불투명도)
  - 같은 색상의 어두운 버전
  - 원래 위치에 희미하게 표시
- **회전 표시**:
  - 리본 스타일의 곡선 화살표 (색상별)
  - 구면 경로를 따라 이전 → 새 위치 연결
  - 그라데이션 페이드 + 글로우 효과
- **각변위**: 15-25도 (각 centroid마다 다름)
- **키워드 벡터**: 밝은 흰색 시머 효과 유지
- **대비**: 밝은 새 위치 vs 어두운 유령 위치

---

## Scene 8: 최종 추천 결과

### 목적
각 조정된 centroid에서 가장 가까운 밴드 1개씩 선택. 선택된 3개 밴드를 강하게 강조.

### Midjourney 프롬프트
```
3D grid space on pure black background, three adjusted centroids as large glowing spheres with halos: cyan-blue, magenta-pink, yellow-orange centroids prominently displayed, all original band spheres shown in very dim gray (backgrounded, 15% opacity), three selected recommendation vectors emphasized: thick bright lines (2.5x width) in cyan, magenta, yellow from origin to selected spheres, selected spheres 1.5x larger with intense glow and pulse effect, glowing connection lines from each centroid to its selected band in matching color with gradient, connection lines solid with particle flow effect, selected bands have bright circular highlight rings around spheres, clear visual hierarchy: centroids largest and brightest, selected bands prominent with thick lines, other vectors extremely faded, dark minimal aesthetic, clean winner indication, vibrant selected elements against black void, isometric perspective, final recommendation visualization --ar 16:9 --style raw --v 6
```

### 세부 설명
- **조정된 Centroid**:
  - 큰 발광 구체 + 헤일로(후광) 효과
  - 시안-블루, 마젠타-핑크, 옐로우-오렌지
  - 가장 크고 밝게 표시
- **비선택 밴드 벡터들**:
  - 매우 어두운 회색 (15% 불투명도)
  - 극도로 희미하게 배경화
- **선택된 3개 밴드**:
  - 굵은 밝은 선 (2.5배 두께) - 각각 시안, 마젠타, 옐로우
  - 구체 1.5배 확대 + 강렬한 글로우 + 펄스 효과
  - 구체 주변에 밝은 원형 강조 링
- **연결선**:
  - 각 centroid → 선택된 밴드
  - 색상 매칭 (시안-시안, 핑크-핑크, 옐로우-옐로우)
  - 실선 + 그라데이션 + 파티클 흐름 효과
- **시각적 계층**:
  1. Centroid (가장 크고 밝음)
  2. 선택된 밴드 (굵고 밝음, 펄스 효과)
  3. 비선택 밴드 (극히 희미함)
- **최종 효과**: 검은 배경에 선택된 3개 요소만 강렬하게 빛남

---

## 공통 스타일 파라미터

### 필수 키워드 (모든 프롬프트)
```
- pure black background / black void
- 3D wireframe grid / 3D grid cube
- dark minimal aesthetic
- isometric view / isometric perspective
- mathematical precision
- clean geometry
- technical visualization
- depth through grid perspective
```

### Midjourney 파라미터
```
--ar 16:9        # 16:9 비율
--style raw      # 기술적 스타일 강조
--v 6            # Midjourney 버전 6
--seed [숫자]    # 일관성 유지 (모든 장면에 동일 seed 사용)
```

### 색상 팔레트
```
- 배경: 순수 검은색 (#000000)
- 그리드: 어두운 회색 (#333333, #444444)
- 벡터 선: 흰색 (#FFFFFF)
- 클러스터 1: 시안-블루 (#00FFFF, #0099FF)
- 클러스터 2: 마젠타-핑크 (#FF00FF, #FF0099)
- 클러스터 3: 옐로우-오렌지 (#FFFF00, #FF9900)
- 키워드 벡터: 밝은 흰색 + 무지개 시머
```

---

## 참고 이미지 스타일 재현을 위한 핵심 요소

### 1. 배경
```
pure black background, no gradient, absolute black (#000000)
```

### 2. 그리드
```
3D wireframe grid cube, thin lines in dark gray (#444444), subtle and not overpowering, perspective depth visible
```

### 3. 벡터 표현
```
- 선: thin white lines, clean and sharp
- 끝점: small glowing spheres with soft radial glow
- 원점에서 출발: all vectors originate from center origin point
```

### 4. 글로우 효과
```
soft radial glow on spheres, NOT too bright, subtle luminescence, glow fades smoothly into black background
```

### 5. 카메라 앵글
```
isometric view at 45 degree angle, consistent perspective across all scenes
```

---

## Midjourney 사용 팁

### 일관성 유지
1. Scene 1에서 마음에 드는 이미지 생성
2. 이미지 우클릭 → "Copy seed"
3. Scene 2-8 프롬프트에 `--seed [복사한숫자]` 추가
4. 동일한 카메라 앵글과 그리드 스타일 유지

### 색상 조정
참고 이미지처럼 더 차분한 색상을 원한다면:
```
pastel cyan-blue, soft magenta-pink, muted yellow-orange, desaturated colors
```

더 강렬한 색상을 원한다면:
```
vibrant cyan, electric magenta, bright yellow, neon-like glow, saturated colors
```

### 그리드 밀도 조정
더 조밀한 그리드:
```
dense grid lines, small grid cells, detailed wireframe
```

더 희미한 그리드:
```
subtle grid lines, minimal grid visibility, faint wireframe
```

### 글로우 강도 조정
약한 글로우:
```
subtle glow, soft luminescence, gentle radiance
```

강한 글로우:
```
intense glow, bright radiance, strong bloom effect, neon-like
```

---

## 영상 제작 가이드

### 타임라인 (20초)
```
Scene 1: 0:00-0:02 (2초) - 초기 상태
Scene 2: 0:02-0:04 (2초) - 클러스터링 시작
Scene 3: 0:04-0:06 (2초) - 클러스터링 완료
Scene 4: 0:06-0:09 (3초) - Centroid 생성
Scene 5: 0:09-0:11 (2초) - 키워드 등장
Scene 6: 0:11-0:14 (3초) - Slerp 경로
Scene 7: 0:14-0:17 (3초) - 회전 완료
Scene 8: 0:17-0:20 (3초) - 최종 추천
```

### 전환 효과
- **Cross Dissolve**: 0.3초 (대부분의 전환)
- **Fade to Black**: Scene 4→5 (키워드 등장 전 강조)

### 애니메이션 추가 (After Effects / Blender)
- **Scene 1**: 구체들이 하나씩 나타나며 페이드 인
- **Scene 2-3**: 구체 색상이 서서히 변화
- **Scene 4**: Centroid가 스케일 업 + 글로우 강화
- **Scene 5**: 키워드 벡터가 날아오는 모션 (파티클 트레일)
- **Scene 6**: 아크 경로가 점진적으로 그려짐
- **Scene 7**: Centroid들이 실제로 회전하는 애니메이션
- **Scene 8**: 선택된 밴드에 펄스 효과

### 배경음악
- **스타일**: Dark Ambient, Minimal Techno, Electronic
- **분위기**: 우주적, 수학적, 미래적
- **추천 아티스트 스타일**: 
  - Carbon Based Lifeforms (ambient)
  - Stephan Bodzin (melodic techno)
  - Max Cooper (data-driven electronic)

---

## 문제 해결

### 문제: 그리드가 너무 밝게 나옴
**해결**:
```
extremely dark gray grid (#222222), barely visible grid, ultra subtle wireframe
```

### 문제: 배경이 완전히 검지 않음
**해결**:
```
pure black background, absolute black void, no ambient light, complete darkness except for elements
```

### 문제: 구체 글로우가 과도함
**해결**:
```
subtle soft glow, gentle radiance, minimal bloom effect, controlled luminescence
```

### 문제: 색상이 너무 형광색으로 나옴
**해결**:
```
desaturated colors, muted tones, pastel colors, NOT neon, refined color palette
```

### 문제: 벡터선이 너무 굵게 나옴
**해결**:
```
thin white lines, hair-thin vectors, delicate line work, 1-pixel width appearance
```

---

## 최종 체크리스트

- [ ] 모든 장면에 동일한 `--seed` 값 사용
- [ ] 배경이 순수 검은색인지 확인
- [ ] 그리드가 참고 이미지처럼 희미한지 확인
- [ ] 구체 글로우가 과하지 않고 적절한지 확인
- [ ] 색상이 서로 잘 구분되는지 확인
- [ ] 카메라 앵글이 모든 장면에서 일관된지 확인
- [ ] 고해상도 업스케일 완료
- [ ] 영상 편집 소프트웨어 준비
- [ ] 배경음악 선택 완료

---

## 참고 이미지 스타일 핵심 요약

**DO (해야 할 것)**:
- ✅ 순수 검은색 배경
- ✅ 희미한 회색 그리드
- ✅ 얇은 흰색 벡터선
- ✅ 끝점에 작은 발광 구체
- ✅ 부드러운 글로우 효과
- ✅ 깔끔한 미니멀 구성

**DON'T (하지 말아야 할 것)**:
- ❌ 밝은 배경
- ❌ 굵은 화살표
- ❌ 과도한 네온 효과
- ❌ 복잡한 텍스처
- ❌ 사실적인 3D 렌더링
- ❌ 불필요한 장식 요소

이 프롬프트들로 참고 이미지와 유사한 다크하고 세련된 스타일의 알고리즘 시각화를 만들 수 있습니다!
