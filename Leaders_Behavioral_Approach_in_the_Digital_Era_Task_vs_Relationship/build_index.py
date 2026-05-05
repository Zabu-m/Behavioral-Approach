import os
import re

def generate_index():
    # Klasördeki "page_X.html" şeklindeki dosyaları bul
    html_files = [f for f in os.listdir('.') if re.match(r'^page_\d+\.html$', f)]
    
    if not html_files:
        print("Hata: Bu klasörde 'page_1.html', 'page_2.html' gibi isimlendirilmiş dosyalar bulunamadı.")
        return

    # Toplam slayt sayısını bul
    total_slides = len(html_files)
    print(f"Toplam {total_slides} adet slayt bulundu. index.html oluşturuluyor...")

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Presentation Slides</title>
    <style>
        body, html {{
            margin: 0;
            padding: 0;
            width: 100%;
            height: 100%;
            overflow: hidden;
            background-color: #222;
        }}
        #slideContainer {{
            position: absolute;
            top: 50%;
            left: 50%;
            width: 1280px;
            height: 720px;
            margin-left: -640px; 
            margin-top: -360px;
            transform-origin: center center;
        }}
        iframe {{
            width: 100%;
            height: 100%;
            border: none;
            display: block;
            background-color: #FDFBF7;
        }}
        #clickOverlay {{
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            z-index: 5;
            cursor: pointer;
        }}
        #controls {{
            position: absolute;
            bottom: 20px;
            right: 20px;
            z-index: 10;
            color: rgba(255, 255, 255, 0.9);
            font-family: sans-serif;
            background: rgba(0, 0, 0, 0.6);
            padding: 10px 15px;
            border-radius: 8px;
            user-select: none;
            font-size: 14px;
            display: flex;
            align-items: center;
            gap: 15px;
        }}
        #controls span {{
            font-weight: bold;
            color: white;
        }}
        #fullscreenBtn {{
            background: rgba(255, 255, 255, 0.2);
            border: 1px solid rgba(255, 255, 255, 0.4);
            color: white;
            padding: 5px 10px;
            border-radius: 4px;
            cursor: pointer;
            font-size: 13px;
            font-weight: bold;
        }}
        #fullscreenBtn:hover {{
            background: rgba(255, 255, 255, 0.3);
        }}
    </style>
</head>
<body>
    <div id="slideContainer">
        <iframe id="slideFrame" src="page_1.html"></iframe>
    </div>
    <div id="clickOverlay"></div>
    <div id="controls">
        <button id="fullscreenBtn" title="Tam Ekran">⛶ Tam Ekran</button>
        <div>Slide: <span id="currentSlide">1</span> / {total_slides}</div>
    </div>

    <script>
        var totalSlides = {total_slides};
        var currentSlide = 1;
        var slideFrame = document.getElementById("slideFrame");
        var slideIndicator = document.getElementById("currentSlide");
        var fullscreenBtn = document.getElementById("fullscreenBtn");
        var slideContainer = document.getElementById("slideContainer");
        var clickOverlay = document.getElementById("clickOverlay");
        var touchStartX = null;
        var touchStartY = null;
        var lastTouchTime = 0;

        function resizeContainer() {{
            var scale = Math.min(window.innerWidth / 1280, window.innerHeight / 720);
            slideContainer.style.transform = "scale(" + scale + ")";
        }}

        window.addEventListener('resize', resizeContainer);
        resizeContainer();

        function updateSlide(newSlide) {{
            if (newSlide >= 1 && newSlide <= totalSlides) {{
                currentSlide = newSlide;
                slideFrame.src = "page_" + currentSlide + ".html";
                slideIndicator.textContent = currentSlide;
            }}
        }}

        function nextSlide() {{
            if (currentSlide < totalSlides) {{
                updateSlide(currentSlide + 1);
            }}
        }}

        function prevSlide() {{
            if (currentSlide > 1) {{
                updateSlide(currentSlide - 1);
            }}
        }}

        function isControlInteraction(target) {{
            return target.closest && target.closest("#controls");
        }}

        function handleTapNavigation(target, clientX) {{
            if (isControlInteraction(target)) return;
            var viewportWidth = window.innerWidth || document.documentElement.clientWidth;
            if (clientX < viewportWidth * 0.35) {{
                prevSlide();
            }} else {{
                nextSlide();
            }}
        }}

        function handleKeydown(e) {{
            if (e.code === "Space" || e.code === "ArrowRight" || e.code === "ArrowDown" || e.code === "PageDown") {{
                e.preventDefault();
                nextSlide();
            }} else if (e.code === "ArrowLeft" || e.code === "ArrowUp" || e.code === "PageUp") {{
                e.preventDefault();
                prevSlide();
            }}
        }}

        function handleMousedown(e) {{
            if (isControlInteraction(e.target)) return;

            if (e.button === 0) {{ 
                handleTapNavigation(e.target, e.clientX);
            }} else if (e.button === 2) {{ 
                prevSlide();
            }}
        }}

        function handleClick(e) {{
            if (Date.now() - lastTouchTime < 500) return;
            handleTapNavigation(e.target, e.clientX);
        }}

        function handleTouchstart(e) {{
            if (isControlInteraction(e.target) || e.touches.length !== 1) return;
            var touch = e.touches[0];
            touchStartX = touch.clientX;
            touchStartY = touch.clientY;
        }}

        function handleTouchend(e) {{
            if (touchStartX === null || touchStartY === null || e.changedTouches.length === 0) return;

            var touch = e.changedTouches[0];
            var deltaX = touch.clientX - touchStartX;
            var deltaY = touch.clientY - touchStartY;
            var absX = Math.abs(deltaX);
            var absY = Math.abs(deltaY);
            var swipeThreshold = 35;
            var tapThreshold = 10;

            if (absX > swipeThreshold && absX > absY) {{
                if (deltaX < 0) {{
                    nextSlide();
                }} else {{
                    prevSlide();
                }}
                lastTouchTime = Date.now();
                e.preventDefault();
            }} else if (absX < tapThreshold && Math.abs(deltaY) < tapThreshold) {{
                handleTapNavigation(e.target, touch.clientX);
                lastTouchTime = Date.now();
                e.preventDefault();
            }}

            touchStartX = null;
            touchStartY = null;
        }}

        function handleContextmenu(e) {{
            e.preventDefault(); 
        }}

        fullscreenBtn.addEventListener("click", function(e) {{
            if (!document.fullscreenElement) {{
                document.documentElement.requestFullscreen().catch(function(err) {{
                    console.log("Tam ekrana geçilemedi:", err);
                }});
            }} else {{
                if (document.exitFullscreen) {{
                    document.exitFullscreen();
                }}
            }}
        }});

        window.addEventListener("keydown", handleKeydown);
        clickOverlay.addEventListener("mousedown", handleMousedown);
        clickOverlay.addEventListener("click", handleClick);
        clickOverlay.addEventListener("touchstart", handleTouchstart, {{ passive: true }});
        clickOverlay.addEventListener("touchend", handleTouchend, {{ passive: false }});
        window.addEventListener("contextmenu", handleContextmenu);
        
    </script>
</body>
</html>"""

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
        
    print("index.html dosyası başarıyla oluşturuldu!")

if __name__ == "__main__":
    generate_index()
