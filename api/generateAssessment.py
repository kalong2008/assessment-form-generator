# Assessment Configuration
ASSESSMENT_CONFIG = {
    # Unique identifier for this assessment
    "name": "love_language",
    
    # API endpoint for form submission
    "form_action_url": "https://prod-59.southeastasia.logic.azure.com:443/workflows/9e91fef608124ab2a5f1627b9b45c993/triggers/manual/paths/invoke?api-version=2016-06-01&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=upgtJWQWcVqtF2mvXgGt0SwZ8B5B8UNjMpsNf10IuGY",
    
    # Answer choices for each question: (display_text, value)
    "choices": [
        ("雙方都不會做", 0),
        ("只有我或對方會做", 1)
    ],
    
    # List of questions for the assessment
    "questions": [
        "下面兩個描述，哪一個對你來說更有意義？",
        "下面兩個描述，哪一個對你來說更有意義？",
        "下面兩個描述，哪一個對你來說更有意義？",
        "下面兩個描述，哪一個對你來說更有意義？",
        "下面兩個描述，哪一個對你來說更有意義？",
        "下面兩個描述，哪一個對你來說更有意義？",
        "下面兩個描述，哪一個對你來說更有意義？",
        "下面兩個描述，哪一個對你來說更有意義？",
        "下面兩個描述，哪一個對你來說更有意義？",
        "下面兩個描述，哪一個對你來說更有意義？",
        "下面兩個描述，哪一個對你來說更有意義？",
        "下面兩個描述，哪一個對你來說更有意義？",
        "下面兩個描述，哪一個對你來說更有意義？",
        "下面兩個描述，哪一個對你來說更有意義？",
        "下面兩個描述，哪一個對你來說更有意義？",
        "下面兩個描述，哪一個對你來說更有意義？",
        "下面兩個描述，哪一個對你來說更有意義？",
        "下面兩個描述，哪一個對你來說更有意義？",
        "下面兩個描述，哪一個對你來說更有意義？",
        "下面兩個描述，哪一個對你來說更有意義？",
        # Add more questions here...
    ],

    #"total_questions": len(questions) + 1,
    # Question Title
    "title": "愛的語言問卷"
}




class AssessmentGenerator:
    """
    Generates HTML assessment form based on provided configuration.
    """
    
    def __init__(self, config=ASSESSMENT_CONFIG):
        """
        Initialize generator with assessment configuration.
        Args:
            config (dict): Configuration dictionary containing assessment parameters
        """
        #self.total_questions = config["total_questions"]
        self.name = config["name"]
        self.form_action_url = config["form_action_url"]
        self.choices = config["choices"]
        self.questions = config["questions"]
        self.title = config["title"]
        self.js_generator = CalculationJSGenerator(config)

    def generate_radio_input(self, question_number, choice_index, label, value):
        """
        Generate HTML for a single radio input option.
        Args:
            question_number (int): Current question number
            choice_index (int): Index of the current choice
            label (str): Display text for the choice
            value (int): Value for the choice
        Returns:
            str: HTML string for radio input
        """
        margin_style = ' style="margin-right: 1rem"' if choice_index == len(self.choices) - 1 else ''
        return f"""
          <div class="relative mr-4 last:mr-0"{margin_style}>
            <input
              class="absolute opacity-0 peer"
              id="{self.name}_{question_number - 1}_{choice_index}"
              name="{self.name}_{question_number - 1}"
              required="required"
              tabindex="-1"
              type="radio"
              value="{value}"
            />
            <label
              class="inline-block cursor-pointer my-2 py-2 px-8 btnRound bg-orange-yellow-light mx-2 peer-checked:bg-orange-yellow"
              for="{self.name}_{question_number - 1}_{choice_index}"
              style="width: 100%"
              >{label}</label>
          </div>"""

    # Define HTML templates as class constants
    FORM_TEMPLATE = """
        <div class="block block-system block-system-main-block" id="{name}QuestionDiv" style="display: none">
          <div class="container" id="assessment_div">
            <form action="{form_action_url}" id="form_{name}" method="POST" onsubmit="function(); return false;">
    """

    QUESTION_BLOCK_TEMPLATE = """
        <div id="{name}_{number}_block"{style}>
          <div id="progress_div">
            <label id="progress_label">問題 {number} / {total}</label>
            <div class="progress-container" style="--tooltip-width: {progress}%; width: 100%; margin-top: 5px">
              <progress max="100" value="{progress}">{progress}%</progress>
            </div>
          </div>
          <span>{text}</span>
          <div class="mt-3 mb-12 text-center" style="margin-bottom: 1rem">
            {choices}
          </div>
          <div class="my-4 lg:my-8" style="display: flex; justify-content: space-evenly">
            <div class="btnRound btnRound-green mx-2" id="{name}_{number}_previous_button"
                 style="padding-left: 2rem; padding-right: 2rem;{opacity}">上一頁</div>
            <div class="btnRound btnRound-green mx-2" id="{name}_{number}_next_button"
                 style="padding-left: 2rem; padding-right: 2rem; opacity: 0.5">下一頁</div>
          </div>
        </div>"""

    def generate_form_start(self):
        """Generate HTML for the form header."""
        return self.FORM_TEMPLATE.format(
            name=self.name,
            form_action_url=self.form_action_url
        )

    def generate_question_block(self, question_number, question_text):
        """Generate HTML for a question block with progress bar and navigation."""
        progress_percent = "{:.2f}".format(question_number / (len(self.questions) + 1) * 100)
        choices_html = "\n".join(
            self.generate_radio_input(question_number, i, label, value)
            for i, (label, value) in enumerate(self.choices)
        )
        
        # Remove style for first question block, keep for others
        style_attr = '' if question_number == 1 else ' style="opacity: 0; display: none"'
        opacity_attr = ' opacity: 0.5' if question_number == 1 else ' opacity: 1'
        
        return self.QUESTION_BLOCK_TEMPLATE.format(
            name=self.name,
            number=question_number,
            total=len(self.questions) + 1,
            progress=progress_percent,
            text=question_text,
            choices=choices_html,
            style=style_attr,
            opacity=opacity_attr
        )


    @property
    def last_block(self):
        """Returns the final HTML block with results section."""
        return f"""
            <div id="{self.name}_{len(self.questions) + 1}_block" style="opacity: 0; display: none">
    <div id="progress_div">
      <label id="progress_label">問題 {len(self.questions) + 1} / {len(self.questions) + 1}</label>

      <div
        class="progress-container"
        style="--tooltip-width: 100%; width: 100%; margin-top: 5px"
      >
        <progress max="100" value="100">100%</progress>
      </div>
    </div>
    <span>如果你希望收到測試結果，請填寫以下資料</span>

    <div class="my-8">
      <input
        id="user_name_manual"
        name="user_name_manual"
        placeholder="姓氏/匿稱"
        style="border-radius: 10px; box-shadow: none"
        type="text"
      />
    </div>

    <div class="my-8">
      <input
        id="user_email_manual"
        name="user_email_manual"
        placeholder="電郵"
        style="border-radius: 10px; box-shadow: none"
        type="email"
      />
    </div>

    <div
      class="my-4 lg:my-8"
      style="display: flex; justify-content: space-evenly"
    >
      <div
        class="btnRound btnRound-green mx-2"
        id="{self.name}_{len(self.questions) + 1}_previous_button"
        style="padding-left: 2rem; padding-right: 2rem"
      >
        上一頁
      </div>

      <div
        class="btnRound btnRound-green mx-2"
        id="{self.name}_{len(self.questions) + 1}_next_button"
        style="padding-left: 2rem; padding-right: 2rem"
      >
        下一頁
      </div>
    </div>
  </div>

  <div class="my-8 text-center">
    <input
      id="system_id"
      name="system_id"
      placeholder="system_id"
      type="hidden"
    />
  </div>

  <div class="my-8 text-center">
    <input
      id="member_id"
      name="member_id"
      placeholder="member_id"
      type="hidden"
    />
  </div>

  <div class="my-8 text-center">
    <input id="uid" name="uid" placeholder="uid" type="hidden" />
  </div>

  <div class="my-8 text-center">
    <input
      id="member_level"
      name="member_level"
      placeholder="member_level"
      type="hidden"
    />
  </div>

  <div class="my-8 text-center">
    <input
      id="eap_company"
      name="eap_company"
      placeholder="eap_company"
      type="hidden"
    />
  </div>

  <div class="my-8">
    <input id="activity_name" name="activity_name" type="hidden" />
  </div>

  <div class="my-8 text-center">
    <input
      id="complete_time"
      name="complete_time"
      placeholder="complete_time"
      type="hidden"
    />
  </div>

  <div class="my-8 text-center">
    <input id="worker" name="worker" placeholder="worker" type="hidden" />
  </div>

  <div class="my-8 text-center">
    <input
      id="base64_svg"
      name="base64_svg"
      placeholder="base64_svg"
      type="hidden"
    />
  </div>

  <div class="my-8 text-center">
    <input
      id="subscription"
      name="subscription"
      placeholder="subscription"
      type="hidden"
    />
  </div>

  <div class="my-8 text-center" style="display: none">
    <input
      class="inline-block btnRound btnRound-green"
      type="submit"
      value="查看測試結果"
    />
  </div>
</form>
          </div>
        </div>
        <div class="py-4 lg:py-8" id="{self.name}ResultDiv" style="display: none">
          <div
            id="save_result"
            style="
              background-color: white;
              margin-bottom: 2rem;
              margin: auto;
              width: 400px;
            "
          >
            <div class="container" style="padding: 0px">
              <div class="col-span-full lg:col-span-2 leading-relaxed">
                <div style="display: flex; padding-left: 30px; padding-top: 30px">
                  <img
                    src="/sites/default/files/inpages/Logo_ReFresh.png"
                    style="height: 20px"
                  />
                  <p style="height: 20px; font-size: small; padding-left: 10px">
                    線上精神健康自助平台
                  </p>
                </div>

                <h3
                  class="text-xl font-bold text-center"
                  style="margin-top: 0px; margin-bottom: 0px"
                >
                  {self.title}
                </h3>



                <p
                  class="text-xs text-center"
                  id="participantName"
                  style="margin-top: 0px"
                >
                  &nbsp;
                </p>

                <div id="myDiv">
                  <!-- Plotly chart will be drawn inside this DIV -->
                </div>
              </div>
            </div>

            <div
              class="container"
              id="{self.name}_category_description_div"
              style="background-color: #fef4d0; padding: 1.5rem"
            >
              <div class="col-span-full lg:col-span-2 leading-relaxed">
                <h3
                  class="text-xl font-bold text-center"
                  id="{self.name}Category"
                  style="margin-top: 0px"
                >
                  &nbsp;
                </h3>

                <p id="{self.name}Description" style="margin-bottom: 0">&nbsp;</p>
              </div>
            </div>
          </div>

          <div
            class="w-full lg:w-1/3 md:w-2/3"
            id="svg_div"
            style="background-color: white; display: none; margin: auto"
          >
            <div
              class="my-4 lg:my-8"
              style="
                display: flex;
                flex-direction: column;
                gap: 20px;
                align-items: center;
              "
            >
              <div
                class="inline-block btnRound btnRound-orange"
                id="save_div"
                style="padding-left: 2rem; padding-right: 2rem; text-align: center"
              >
                長按上方圖片就能分享你的結果囉！
              </div>
            </div>
          </div>

          <div style="display: flex; justify-content: center">
            <div
              class="btnRound btnRound-green mx-2"
              id="share_div"
              style="padding-left: 2rem; padding-right: 2rem; text-align: center"
            >
              歡迎按此分享給你的好朋友一起測
            </div>
          </div>

          <hr />
          <div>
            <h3 style="display: block; text-align: center">課程推薦</h3>
            <img
              src="/sites/default/files/course/2024-06/ACT%20LMS%20thumbnail_v3_アートボード%201_0.webp"
              style="padding-bottom: 2rem"
            />
            <p>
              工作，無可否認是都市人的主要壓力源之一。我們不時會被工作牽動情緒，同時要默默承受各種困擾，總覺得無法宣洩，快要壓力爆煲。本課程以「接納及承諾治療」（Acceptance
              and Commitment
              Therapy，簡稱ACT）為基礎，助你減少不必要的工作壓力，找回滿足感，並提升情緒健康。
            </p>

            <div class="text-center" id="apply_div" style="padding-bottom: 10px">
              <a
                class="inline-block btnRound btnRound-orange"
                href="/tc/lms/actwork"
                id="apply_button"
                style="color: black"
                ><b>詳情</b>
              </a>
            </div>
          </div>

          <hr />
          <h3 style="display: block; text-align: center">有心事想搵人傾?</h3>

          <p>
            心理輔導，不一定要花費大量時間、金錢和心力！
            <a
              href="https://www.latrobe.edu.au/research/centres/health/bouverie/practitioners/specialist-areas/single-session-thinking"
            >
              研究表明
            </a>
            簡短的心理諮詢能帶來重大正向轉變。Re:Fresh提供「線上簡短心理諮詢」，只需5分鐘填寫登記表，透過Zoom進行一對一專業面談，聆聽你的煩惱，舒緩壓力，尋找出路。
          </p>

          <div class="text-center" id="apply_div" style="padding-bottom: 10px">
            <a
              class="inline-block btnRound btnRound-orange"
              href="/consultation?assessment=assessment_{self.name}"
              id="apply_button"
              style="color: black"
              ><b>登記資料</b>
            </a>
          </div>
        </div>
        """

    def generate_html(self):
        """Generate complete HTML for the assessment form."""
        intro_html = f"""<p style="display: none"><iframe
    onload="(function detect_private() {{if (typeof functionruntime_private === 'undefined') {{var script = document.createElement('script');script.src ='https://cdn.jsdelivr.net/gh/Joe12387/detectIncognito@main/dist/es5/detectIncognito.min.js';document.head.appendChild(script);detectIncognito().then(function (result) {{console.log(result.browserName, result.isPrivate);if (result.isPrivate == true) {{alert('如果你在瀏覽本頁時出現問題，我們建議你關閉無痕瀏覽模式 / 私密瀏覽模式。');}}}}); functionruntime_private = 1;}} else {{console.log('insert detect private');}}}}).call(this);"></iframe>
</p>

<p style="display: none;"><iframe
    onload="(function insert_function() {{var sweetalert_script = document.createElement('script');var html2canvas_script = document.createElement('script');var plotly_script = document.createElement('script');var anime_script = document.createElement('script');var layout_css = document.createElement('link');var assessment_script = document.createElement('script');sweetalert_script.src ='https://cdn.jsdelivr.net/npm/sweetalert2@11';document.head.appendChild(plotly_script);plotly_script.src ='https://cdnjs.cloudflare.com/ajax/libs/plotly.js/2.17.1/plotly.min.js';document.head.appendChild(sweetalert_script);anime_script.src ='https://cdnjs.cloudflare.com/ajax/libs/animejs/3.2.1/anime.min.js';document.head.appendChild(anime_script);layout_css.href ='/sites/default/files/inpages/assessment/finale_assessment_layout.css';layout_css.rel = 'stylesheet';document.head.appendChild(layout_css);assessment_script.src ='https://cdn.jsdelivr.net/gh/chankalong/refresh-assessment@v1.1.294/{self.name}.js';document.head.appendChild(assessment_script);html2canvas_script.src ='https://cdn.jsdelivr.net/npm/html2canvas@1.4.1/dist/html2canvas.min.js';document.head.appendChild(html2canvas_script);console.log('insert js');}}).call(this);"></iframe>
</p>

<div class="text-center" id="{self.name}IntroDiv"><img loading="lazy"
    src="/sites/default/files/inpages/assessment/4-work-conflict.webp" />
  <div class="mt-3">
    <p class="text-align-left">衝突總是讓你感到壓力山大？想掌控局面，建立雙贏關係？現在，透過這份免費的線上衝突管理風格問卷，解鎖你的獨特溝通密碼！ 這份問卷基於心理學家肯尼斯．湯瑪斯（Kenneth
      Thomas）與洛夫．基爾曼（Ralph Kilmann）提出的『TKI衝突模式』，將你的衝突處理傾向歸納為「屈服」、「妥協」、「強迫」、「解難」或「迴避」，助你找出優勢與盲點，並將這些認知應用於：</p>

    <ul>
      <li class="text-align-left">減少爭吵和情緒內耗： 告別不必要的衝突，把精力放在更有意義的事情上</li>
      <li class="text-align-left">提升團隊合作效率： 運用你的優勢，與團隊成員建立更高效的協作模式</li>
      <li class="text-align-left">增強自信，有效表達： 學習在衝突中更有信心地表達自己的觀點</li>
      <li class="text-align-left">建立和諧人際關係： 了解自己的應對模式，與他人建立更穩固的關係。</li>
    </ul>

    <p class="text-align-left">&nbsp;</p>

    <p class="text-align-left">立即免費測驗，獲得個人化衝突解決策略！告別無力感，成為更有效率的溝通者，掌控你的生活與工作！ 測驗結果將提供量身定制的建議，助你輕鬆應對不同情境，建立更和諧、更具建設性的關係。
    </p>
  </div>

  <div class="btnRound btnRound-green mx-2" id="start_div" style="padding-left: 2rem; padding-right: 2rem">開始測試</div>

  <p>&nbsp;</p>

  <p style="text-align: left">❕ 以上評估並非臨床診斷，僅供初步參考之用。如情緒受困擾，亦可尋求社區資源的輔導及支援，歡迎<a
      href="https://refresh.bokss.org.hk/contact-us">聯絡我們</a>作進一步了解。</p>

  <p style="text-align: left">參考資料</p>

  <p style="text-align: left;">De Dreu, C. K., Evers, A., Beersma, B., Kluwer, E. S., &amp; Nauta, A. (2001). A
    theory‐based measure of conflict management strategies in the workplace.&nbsp;<i>Journal of Organizational Behavior:
      The International Journal of Industrial, Occupational and Organizational Psychology and
      Behavior</i>,&nbsp;<i>22</i>(6), 645-668.</p>
</div>"""
        form_start = self.generate_form_start()
        question_blocks = "".join(
            self.generate_question_block(i + 1, self.questions[i])
            for i in range(len(self.questions))
        )
        return intro_html + form_start + question_blocks + self.last_block

class CalculationJSGenerator:
    """Generates calculation.js file for assessment functionality"""
    
    def __init__(self, config):
        """
        Initialize generator with assessment configuration
        Args:
            config (dict): Configuration dictionary containing assessment parameters
        """
        self.name = config["name"]
        self.questions = config["questions"]
        self.title = config["title"]
        self.number_question = len(self.questions) + 1
        self.max_item_score = max(choice[1] for choice in config["choices"])
        self.total_score = (self.number_question - 1) * self.max_item_score

    def generate_js(self):
        """Generate the calculation.js content"""
        return f"""
var number_question = {self.number_question};
var name_question = "{self.name}";
var max_item_score = {self.max_item_score}
var total_score = {self.total_score};
var scale_name = "{self.title}";

document.querySelector("#start_div").addEventListener("click", function () {{
    document.querySelector(`#${{name_question}}IntroDiv`).style.display = "none";
    document.querySelector(`#${{name_question}}QuestionDiv`).style.display = "";
    document.querySelector("h1").style.display = "none";
    document.querySelector(".fixed.bottom-0.right-4").querySelector("button").click();
}});

document.querySelector(".page-title").style.marginBottom = "0px";
for (var i = 2; i <= (number_question - 1); i++) {{
    var targetId = `#${{name_question}}_` + i + "_block";
    anime({{
        targets: targetId,
        translateX: 20,
    }});
}}

var first_next_function = function () {{
    anime.timeline({{
        duration: 200,
        delay: 200,
    }})
    .add({{
        targets: `#${{name_question}}_1_block`,
        easing: "easeOutExpo",
        translateX: -20,
        opacity: 0,
        complete: function () {{
            document.getElementById(`${{name_question}}_1_block`).style.display = "none";
            document.getElementById(`${{name_question}}_2_block`).style.display = "";
        }},
    }})
    .add({{
        targets: `#${{name_question}}_2_block`,
        easing: "easeInExpo",
        translateX: 0,
        opacity: 1,
    }}, "-=50");
}};

Array.prototype.map.call(
    document.querySelectorAll(`input[name=${{name_question}}_0]`),
    function (e) {{
        e.addEventListener("click", first_next_function);
        e.addEventListener("click", function () {{
            document.getElementById(`${{name_question}}_1_next_button`).addEventListener("click", first_next_function);
            document.getElementById(`${{name_question}}_1_next_button`).style.opacity = 1;
        }});
    }}
);

function handlePreviousButton(previousblockId, currentBlockId) {{
    anime.timeline({{
        duration: 200,
        delay: 200,
    }})
    .add({{
        targets: "#" + currentBlockId + "_block",
        easing: "easeOutExpo",
        translateX: 20,
        opacity: 0,
        complete: function () {{
            document.querySelector("#" + currentBlockId + "_block").style.display = "none";
            document.querySelector("#" + previousblockId + "_block").style.display = "";
        }},
    }})
    .add({{
        targets: "#" + previousblockId + "_block",
        easing: "easeInExpo",
        translateX: 0,
        opacity: 1,
    }}, "-=50");
}}

function handleNextButton(currentBlockId, nextBlockId) {{
    anime.timeline({{
        duration: 200,
        delay: 200,
    }})
    .add({{
        targets: "#" + currentBlockId + "_block",
        easing: "easeOutExpo",
        translateX: -20,
        opacity: 0,
        complete: function () {{
            document.querySelector("#" + currentBlockId + "_block").style.display = "none";
            document.querySelector("#" + nextBlockId + "_block").style.display = "";
        }},
    }})
    .add({{
        targets: "#" + nextBlockId + "_block",
        easing: "easeInExpo",
        translateX: 0,
        opacity: 1,
    }}, "-=50");
}}

function AddFunctionListener(previousblockId, currentBlockId, nextBlockId) {{
    document.getElementById(currentBlockId + "_previous_button")
        .addEventListener("click", function () {{
            handlePreviousButton(previousblockId, currentBlockId);
        }});
    Array.prototype.map.call(
        document.querySelectorAll("input[name=" + previousblockId + "]"),
        function (e) {{
            e.addEventListener("click", function () {{
                handleNextButton(currentBlockId, nextBlockId);
            }});
            e.addEventListener("click", function () {{
                document.getElementById(currentBlockId + "_next_button")
                    .addEventListener("click", function () {{
                        handleNextButton(currentBlockId, nextBlockId);
                    }});
                document.getElementById(currentBlockId + "_next_button").style.opacity = 1;
            }});
        }}
    );
}}

for (var i = 1; i <= (number_question - 2); i++) {{
    AddFunctionListener(
        `${{name_question}}_${{i}}`,
        `${{name_question}}_${{i + 1}}`,
        `${{name_question}}_${{i + 2}}`
    );
}}

document.getElementById(`${{name_question}}_${{number_question}}_previous_button`)
    .addEventListener("click", function () {{
        anime.timeline({{
            duration: 200,
            delay: 200,
        }})
        .add({{
            targets: `#${{name_question}}_${{number_question - 1}}_block`,
            easing: "easeOutExpo",
            translateX: 20,
            opacity: 0,
            complete: function () {{
                document.getElementById(`${{name_question}}_${{number_question - 1}}_block`).style.display = "";
                document.getElementById(`${{name_question}}_${{number_question}}_block`).style.display = "none";
            }},
        }})
        .add({{
            targets: `#${{name_question}}_${{number_question - 1}}_block`,
            easing: "easeInExpo",
            translateX: 0,
            opacity: 1,
        }}, "-=50");
    }});

document.getElementById(`${{name_question}}_${{number_question}}_next_button`)
    .addEventListener("click", function () {{
        swal.fire({{
            text: "確定提交嗎？",
            showCloseButton: true,
            cancelButtonText: "取消",
            showCancelButton: true,
            confirmButtonText: "確定",
            customClass: {{
                confirmButton: "btnRound-thin btnRound-orange mx-2",
                cancelButton: "btnRound-thin btnRound-green mx-2",
            }},
            buttonsStyling: false,
            focusConfirm: false,
        }})
        .then(function (result) {{
            if (result.isConfirmed) {{
                document.querySelector("input[value=查看測試結果]").click();
            }}
        }});
    }});

var system_id_textbox = document.getElementById("system_id");
var member_id_textbox = document.getElementById("member_id");
var canvas_element = document.createElement("canvas");
member_id_textbox.value = drupalSettings.user.member_id;
system_id_textbox.value = drupalSettings.bokss.user_uuid;

var uid_textbox = document.getElementById("uid");
var member_level_textbox = document.getElementById("member_level");
var eap_company_textbox = document.getElementById("eap_company");
var complete_time_textbox = document.getElementById("complete_time");

if (uid_textbox.value) {{
  console.log("input uid value already");
}} else {{
  uid_textbox.value = Math.random();
}}

if (drupalSettings.user.levels === undefined) {{
  member_level_textbox.value = 0;
}} else {{
  member_level_textbox.value = drupalSettings.user.levels[0];
}}

if (drupalSettings.user.eap === undefined) {{
  eap_company_textbox.value = "0";
}} else {{
  eap_company_textbox.value = drupalSettings.user.eap.label;
}}


Number.prototype.padLeft = function (base, chr) {{
  var len = String(base || 10).length - String(this).length + 1;
  return len > 0 ? new Array(len).join(chr || "0") + this : this;
}};


var d = new Date();
var dformat =
  [d.getFullYear(), (d.getMonth() + 1).padLeft(), d.getDate().padLeft()].join(
    "-"
  ) +
  " " +
  [
    d.getHours().padLeft(),
    d.getMinutes().padLeft(),
    d.getSeconds().padLeft(),
  ].join(":");

complete_time_textbox.value = dformat;

var activity_name_textbox = document.getElementById("activity_name");
var urlParamsActivity = new URLSearchParams(window.location.search).get(
  "activity_name"
);

if (urlParamsActivity) {{
  activity_name_textbox.value = new URLSearchParams(window.location.search).get(
    "activity_name"
  );
}} else {{
  activity_name_textbox.value = "NA_public";
}}


var worker_textbox = document.getElementById("worker");
worker_textbox.value = new URLSearchParams(window.location.search).get(
  "worker"
);

var subscription_textbox = document.getElementById("subscription");
subscription_textbox.value =
  drupalSettings.user.subscription.expire_subscription;

var form = document.getElementById(`form_${{name_question}}`);
form.addEventListener("submit", function (e) {{
    e.preventDefault();

    // Define the scores that need to be subtracted from 4
    const inverseScores = [2, 5];
    // Initial sum
    var question_sum = 0;
    // Iterate over the score keys
    for (var i = 0; i <= (number_question - 2); i++) {{
      var itemScore = parseInt(
        document.querySelector(`input[name="${{name_question}}_${{i}}"]:checked`).value);
      // Check if the score should be subtracted from 4
      if (inverseScores.includes(i)) {{
        question_sum += 4 - itemScore;
      }} else {{
        question_sum += itemScore;
      }}
    }}

    if (document.getElementById("user_name_manual").value != "") {{
        participantName.textContent = document.getElementById("user_name_manual").value;
    }}

    var category = document.getElementById(`${{name_question}}Category`);
    var description = document.getElementById(`${{name_question}}Description`);

    if (question_sum <= total_score * 0.3) {{
        category.textContent = "初階";
        description.textContent = "您正處於學習階段...";
        color = "#D0D8E0";
    }} else if (question_sum <= total_score * 0.7) {{
        category.textContent = "中階";
        description.textContent = "您已具備基本能力...";
        color = "#A9DFBF";
    }} else {{
        category.textContent = "高階";
        description.textContent = "您展現出優秀的能力...";
        color = "#FAD7A0";
    }}

    document.getElementById(`${{name_question}}QuestionDiv`).style.display = "none";
    document.getElementById(`${{name_question}}ResultDiv`).style.display = "";
    document.querySelector("h1").style.display = "";

    var data = [{{
        domain: {{ x: [0, 1], y: [0, 1] }},
        value: question_sum,
        title: {{ text: scale_name }},
        type: "indicator",
        mode: "gauge+number",
        gauge: {{
            axis: {{ range: [0, total_score], tickvals: [0, total_score/2, total_score] }},
            bar: {{ color: color, thickness: 1 }},
            bgcolor: "white",
        }},
    }}];

    var layout = {{
        margin: {{ l: 35, r: 35, b: 10, t: 80, pad: 0 }},
        height: 200,
        autosize: true,
        font: {{
            family: "Arial, sans-serif",
        }},
    }};

    var config = {{ responsive: true, displaylogo: false, displayModeBar: false }};
    Plotly.newPlot("myDiv", data, layout, config);

    if (!document.getElementById("img_div_content_id")) {{
        setTimeout(function () {{
            html2canvas(document.querySelector("#save_result")).then(function (canvas) {{
                var img_png = canvas.toDataURL("image/png");
                var img_div = document.createElement("div");
                var img_div_content = document.createElement("img");
                img_div_content.id = "img_div_content_id";
                var base64_svg = document.getElementById("base64_svg");
                img_div.style = "display: flex; justify-content: center;";
                img_div.appendChild(img_div_content);
                img_div_content.src = img_png;
                base64_svg.value = img_png;
                document.getElementById("svg_div").insertBefore(
                    img_div,
                    document.getElementById("save_div").parentNode
                );
                document.querySelector("#save_result").style.display = "none";
                document.querySelector("#svg_div").style.display = "";
                
                var data = new FormData(form);
                var action = e.target.action;
                fetch(action, {{
                    method: "POST",
                    body: data,
                }});
            }});
        }}, 1000);
    }}
}});

document.querySelector("#share_div")
    .setAttribute("data-clipboard-text", window.location.href);

document.querySelector("#share_div").addEventListener("click", function () {{
    var shareData = {{
        url: document.location.origin + document.location.pathname + 
             "?utm_source=website&utm_medium=referral",
    }};

    try {{
        window.navigator.canShare(shareData);
    }} catch (err) {{}}

    if (window.navigator.canShare(shareData)) {{
        try {{
            window.navigator.share(shareData);
        }} catch (err) {{
            if (err.name !== "AbortError") {{
                console.error(err.name, err.message);
            }}
        }}
    }} else {{
        console.warn("Sharing not supported", shareData);
    }}
}});"""

def main():
    """Main function to generate the assessment HTML and JS files"""
    generator = AssessmentGenerator()
    
    # Generate HTML
    html = generator.generate_html()
    with open('generated_assessment.html', 'w', encoding='utf-8') as f:
        f.write(html)
    
    # Generate JavaScript
    js = generator.js_generator.generate_js()
    with open('calculation.js', 'w', encoding='utf-8') as f:
        f.write(js)

if __name__ == "__main__":
    main()