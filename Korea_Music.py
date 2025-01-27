import asyncio
from playwright.async_api import async_playwright
import csv
import os
import re


async def safe_get_text(page, selector, timeout=1000):
    """안정적으로 텍스트를 가져오는 비동기 함수."""
    try:
        return await page.inner_text(selector, timeout=timeout)
    except Exception:
        return None


async def classify_region(title, venue):
    """공연 이름과 장소에 따라 지역을 분류하는 함수."""
    # 먼저 공연 제목을 기반으로 지역을 분류하고, 분류되지 않을 경우 공연 장소를 기준으로 재분류
    region_keywords = {
        "서울": ["서울", "목동", "대학로", "구로", "서대문", "경향아트힐", "서울숲", "성수", "사당", "홍대", "명동", "H씨어터"],
        "경기": ["경기", "광명", "하남", "수원", "고양", "성남", "군포", "화성", "김포", "구리", "광교", "과천", "의정부", "양주", "용인", "안산", "오산",
               "부천", "평택", "시흥", "안양", "파주", "여주", "이천"],
        "인천": ["인천", "계양"],
        "강원": ["강원", "춘천", "원주", "강릉", "삼척"],
        "충북": ["충북", "청주", "충주", "제천"],
        "충남": ["충남", "천안", "아산", "서산", "부여", "보령", "당진", "공주"],
        "대전": ["대전", "평송"],
        "세종": ["세종"],
        "전북": ["전북", "전주", "완주", "군산", "익산"],
        "전남": ["전남", "순천", "광양", "여수", "목포", "나주"],
        "광주": ["광주"],
        "경북": ["경북", "대구", "포항", "경주", "구미", "상주", "안동", "울진", "경산"],
        "경남": ["경남", "창원", "진주", "김해", "양산", "사천", "마산", "함안", "거제"],
        "대구": ["대구"],
        "울산": ["울산"],
        "부산": ["부산"],
        "제주": ["제주"],
    }  # 공연 제목에서 지역을 매칭하기 위한 키워드

    venue_keywords = {
        "서울": ["서울", "선릉아트홀", "아시티스", "대학로", "국립정동극장", "국립국악원", "경희대학교", "금호아트홀", "국립극장", "롯데",
               "예술의전당 [서울]", "블루스퀘어", "JCC", "세종문화회관", "나누", "온쉼표", "소월아트홀", "구로아트밸리", "영산", "로데아트센터",
               "충무", "신영체임버홀", "꿈의숲아트센터", "청담", "마포", "반포", "강북", "노원", "광림", "거암", "모차르트홀", "페리지홀",
               "푸르지오아트홀", "IPAC홀", "코엑스", "예술가의 집", "국립중앙박물관", "굿씨어터", "대원", "광야", "성수", "더 줌", "스튜디오 블루",
               "흰물결", "이화여", "서경대", "연세대", "서강대", "강동", "링크아트센터", "스케치홀", "씨어터 쿰", "경복궁", "공유", "지구인",
               "두산", "올림픽공원", "성균관대", "동덕여대", "백암", "유니버설", "예스24", "봄날아트홀", "JTN", "명륜", "구름아래", "달밤엔씨어터",
               "R&J씨어터", "한전아트센터", "유니플렉스", "예그린씨어터", "KT&G", "예림당", "SH", "윤당", "샤롯데씨어터", "명보", "온맘",
               "신한카드", "스테이지", "후암", "JS", "서연", "더 서울라이티움", "브릭스씨어터", "하마씨어터", "북촌", "롤링홀", "무신사 개러지",
               "세종대", "entry55", "광운대", "홍대", "KBS", "플렉스홀", "클럽온에어", "노들섬", "아틀리에", "살롱 문보우", "웨스트브릿지",
               "CJ아지트", "현대카드", "스페이스", "문래재즈IN", "드림홀", "성동", "리엠", "건국대", "명화", "얼라이브", "스테이지",
               "스카이아트홀", "고척스카이돔", "채널 1969", "복합문화공간에무", "중력장", "수상한창고", "두잇아카펠라", "헤르만", "쌀롱드무지끄",
               "상상나라극장", "관악", "국제아트", "서초", "남산", "생기", "Cafe PPnF", "RED POINT", "세티", "펄스", "삼청각", "재즈런치",
               "성암", "은평", "프리즘", "일신", "영등포", "TINC"],
        "경기": ["경기", "성남", "부천", "수원", "콩치노콩크리트", "TOUCH FIVE", "의정부", "안산", "엠피엠지", "킨텍스", "일산", "김포", "안성",
               "모두누림", "구리", "광교", "과천", "양주", "용인", "오산", "광명", "평택", "시흥", "안양", "파주", "여주", "이천", "남양주", "화성",
               "파닥파닥클럽", "고양", "모던클로이스터"],
        "인천": ["인천", "계양", "부평아트센터", "엘림아트센터", "인스파이어 아레나"],
        "강원": ["춘천", "강원", "원주", "강릉", "삼척"],
        "충북": ["쇠내골", "청주", "충북", "충주", "제천"],
        "충남": ["천안", "충남", "아산", "서산"],
        "대전": ["대전", "평송"],
        "세종": ["세종시", "재즈인"],
        "전북": ["군산", "전주", "완주", "익산"],
        "전남": ["전남", "순천", "광양", "여수", "목포", "나주"],
        "광주": ["광주", "국립아시아문화전당"],
        "경북": ["경북", "포항", "구미", "안동", "경주", "상주", "울진"],
        "경남": ["통영국제음악당", "경상남도", "경남", "창원", "진주", "김해", "양산", "사천", "마산", "함안", "거제"],
        "대구": ["대구", "수성아트피아", "삼국유사교육문화회관"],
        "울산": ["울산"],
        "부산": ["부산", "영화의전당"],
        "제주": ["제주"],
    }  # 공연 장소에서 지역을 매칭하기 위한 키워드

    for region, keywords in region_keywords.items():
        for keyword in keywords:
            if keyword in title:
                return region

    for region, keywords in venue_keywords.items():
        for keyword in keywords:
            if keyword in venue:
                return region

    return None  # 매칭되지 않을 경우 "null" 반환


async def parse_period(period):
    """공연기간을 시작일과 종료일로 분리하고 형식을 YYYY-MM-DD로 변환."""
    try:
        date_pattern = r"(\d{4})[.](\d{2})[.](\d{2})"
        dates = re.findall(date_pattern, period)

        if len(dates) == 2:  # 시작일과 종료일 모두 있는 경우
            start_date = "-".join(dates[0])
            end_date = "-".join(dates[1])
            return start_date, end_date
        elif len(dates) == 1:  # 단일 날짜
            start_date = "-".join(dates[0])
            return start_date, "오픈런" if "오픈런" in period else "N/A"
    except Exception as e:
        print(f"날짜 파싱 오류: {e}")
    return "N/A", "N/A"


async def fetch_performance_details(page, performance, index, next_id):
    try:
        # DOM 안정화를 위해 성능 요소를 다시 로드
        await page.wait_for_timeout(500)
        performance = page.locator("ul.iinf_ls li h4 a").nth(index)

        # 스크롤 동작 대신 요소 클릭
        try:
            await performance.scroll_into_view_if_needed()
            await performance.click()
            print(f"공연 {index + 1}: 상세 페이지로 이동 성공")
            await page.wait_for_selector("div.tibt_bb div.tib h4.tit", timeout=35000)
        except Exception:
            print(f"공연 {index + 1}: 요소가 가시 상태가 되지 않아 건너뜀.")
            return None

        img_url = await page.get_attribute("div.tu p img", "src")
        img_url = f"https://www.kopis.or.kr{img_url}" if img_url else "N/A"
        title = await safe_get_text(page, "div.tibt_bb div.tib h4.tit")
        genre = await safe_get_text(page, "div.tibt_bb div.tib span[class^='cls_bx']")
        period = await safe_get_text(page, "dt:has-text('공연기간') + dd")
        venue = await safe_get_text(page, "dt:has-text('공연장소') + dd")
        age = await safe_get_text(page, "dt:has-text('관람연령') + dd")
        ticket = await safe_get_text(page, "dt:has-text('티켓가격') + dd ul li")
        start_date, end_date = await parse_period(period)
        region = await classify_region(title, venue)

        ticket_urls, ticket_vendors = [], []
        try:
            await page.click("a:has-text('예매처 바로가기')")
            await page.wait_for_selector("div.layerPopCon .btnType01_wrap p a", timeout=16000)
            links = page.locator("div.layerPopCon .btnType01_wrap p a")
            link_count = await links.count()

            for idx in range(link_count):
                href = await links.nth(idx).get_attribute("href")
                text = await links.nth(idx).inner_text()
                ticket_urls.append(href)
                ticket_vendors.append(text)
            await page.click("button.btn_close")
        except Exception:
            pass

        print(f"공연 {index + 1}: 데이터 수집 완료")
        return {
            "performance_id": next_id,
            "image": img_url,
            "title": title.strip(),
            "genre": genre.strip(),
            "city": region,
            "start_date": start_date,
            "end_date": end_date,
            "location": venue.strip(),
            "age": age.strip(),
            "price": ticket.strip(),
            "site": ", ".join(ticket_vendors),
            "link": "; ".join(ticket_urls),
        }
    except Exception as e:
        print(f"공연 {index + 1}: 세부 정보 수집 중 오류 발생: {e}")
        return None


async def save_data_to_csv(data, output_file):
    # 기존 데이터 로드
    existing_data = []
    if os.path.exists(output_file):
        with open(output_file, mode="r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            existing_data = list(reader)

    # 기존 데이터에서 가장 큰 ID를 계산
    next_id = 1
    if existing_data:
        ids = [int(row["performance_id"]) for row in existing_data if
               row.get("performance_id") and row["performance_id"].isdigit()]
        next_id = max(ids) + 1 if ids else 1

    # 새로운 데이터에 ID 추가
    for i, entry in enumerate(data):
        entry["performance_id"] = next_id + i

    # 기존 데이터와 새로운 데이터를 병합
    combined_data = existing_data + data

    # 병합된 데이터를 CSV에 저장
    with open(output_file, mode="w", newline="", encoding="utf-8") as file:
        fieldnames = ["performance_id", "image", "title", "genre", "city", "start_date", "end_date", "location",
                      "age", "price", "site", "link"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(combined_data)
    print(f"CSV 파일 저장 완료: {output_file}")


async def crawl_kopis():
    url = "https://www.kopis.or.kr/por/db/pblprfr/pblprfr.do?menuId=MNU_00019"
    output_file = "Performances.csv"

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.route("**/*", lambda route: route.abort() if route.request.resource_type in ["media", "font"] else route.continue_())

        await page.goto(url, timeout=27000, wait_until="domcontentloaded")
        await page.click("a:has-text('조건 검색')")
        await page.check("input#srchPerfoStatusCode_1")
        await page.click("a:has-text('적용하기')")
        await page.click("a:has-text('국악')")  # 장르선택
        await page.wait_for_timeout(3000)

        try:
            await page.wait_for_selector("ul.iinf_ls li h4 a", timeout=39000)
            print("공연 목록 로드 완료")
        except Exception:
            print("공연 목록이 로드되지 않았습니다. 크롤링을 종료합니다.")
            await browser.close()
            return

        data = []
        while True:
            performances = page.locator("ul.iinf_ls li h4 a")
            count = await performances.count()

            if count == 0:
                print("더 이상 공연 목록이 없습니다. 크롤링을 종료합니다.")
                break

            for i in range(count):
                try:
                    performance = performances.nth(i)
                    result = await fetch_performance_details(page, performance, i, 0)
                    if result:
                        data.append(result)
                        await page.click("div.zi p.btn_wrap a.bt_list", timeout=40000)
                except Exception as e:
                    print(f"공연 {i + 1}: 크롤링 중 오류 발생: {e}")
                    continue

            try:
                # 목록 페이지 로드 확인
                await page.wait_for_selector("ul.iinf_ls li h4 a", timeout=51000)

                next_page_locator = page.locator("a.icv.pbml img[alt='다음페이지']")
                if await next_page_locator.count() > 0:
                    current_url = page.url
                    await next_page_locator.click()
                    await page.wait_for_timeout(3000)  # 다음 페이지 로드 대기

                    # 페이지가 완전히 로드될 때까지 대기
                    await page.wait_for_selector("ul.iinf_ls li h4 a", timeout=43000)

                    # URL이 변경되지 않으면 반복 종료
                    if page.url == current_url:
                        print("다음 페이지로 이동하지 못했습니다. 크롤링을 종료합니다.")
                        break
                else:
                    print("더 이상 페이지가 없습니다. 크롤링을 종료합니다.")
                    break
            except Exception as e:
                print(f"다음 페이지로 이동 중 오류 발생: {e}")
                break

        next_id = 1
        if os.path.exists(output_file):
            with open(output_file, mode="r", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                ids = [int(row["performance_id"]) for row in reader if
                       row.get("performance_id") and row["performance_id"].isdigit()]
                if ids:
                    next_id = max(ids) + 1

        for i, entry in enumerate(data):
            entry["performance_id"] = next_id + i

        await save_data_to_csv(data, output_file)
        await browser.close()


# 크롤러 실행
asyncio.run(crawl_kopis())