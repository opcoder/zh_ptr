中文事件抽取:
1. 任务：
    从自然语言新闻中抽取军事政治事件，抽取结果为：{SOURCE_ACTOR, ACTION_TYPE, TARGET_ACTOR} 和 {DATE_TIME, LOCATION}，即施事者，事件类型，受事者，时间，地点
    其中CAMEO手册(CAMEO.Manual.1.1b3.pdf)对{施事者，事件类型，受事者}均有对应的编码。
    参考CAMEO.eventcodes.txt，帮助大家对“事件”形成初步认识，更深入地了解课参考CAMEO.Manual.1.1b3.pdf第二章VERB CODEBOOK。
2. 参考算法：
   参照英文版抽取方法petrarch2[https://github.com/openeventdata/petrarch2]。
   ACTION_TYPE：即事件编码，采用句法解析+模式匹配的方式进行抽取。句法解析格式参考中文事件抽取20170616.pptx，模式匹配所使用模式参考http://petrarch2.readthedocs.io/en/latest/dictionaries.html#verb-dictionary
   SOURCE_ACTOR，TARGET_ACTOR：比较简单，匹配actor字典。
3. 中文抽取：
    主要分两部分：一是对petrarch2英文抽取代码进行汉化，去除英文特性，增加中文特性；二是汉化petrarch2所使用的字典，包括actor(Phoenix.Countries.actors.txt, Phoenix.Internationak.actors.txt,
    Phoenix.MilNonState.actors.txt, Phoenix.agents.txt)等字典，模式字典(CAMEO.2.0.txt)等。
    目前代码的汉化工作主要由我负责，想参与代码工作的可以跟我联系一下。
    然后是主要工作量集中在字典方面，整个小组需要都参与进来。进行字典构建之前需要进行一些准备工作。
4. 准备工作：
    了解petrarch2的英文事件抽取流程，以及该代码如何使用字典进行事件抽取(主要是利用模式字典进行事件编码)。不要求了解代码具体细节。
    除上面介绍以外，还可以参考：
        petrarch2[https://github.com/openeventdata/petrarch2]及其文档。
        Petrarch2.pdf
        PETRARCH流程及接口说明.pdf
5. 当前任务：
    5.1 模式字典(CAMEO.2.0.txt)的翻译和构建
    5.2 一个栗子
        ```
        ---  CALL   [041:041]  ---  # 动词解释
        CALL # 同义词
        PHONE # 同义词
        TELEPHONE # 同义词
        - * POWDER KEG                                        [012]         # CALL， 模式句型， * 代表动词所在位置
        - * PARTNER                                           [013]         # CALL
        - * SESSION                                           [014]         # CALL
        - * HELP                                              [020]         # CALL
        - * (FOR PROTECTION)                                  [0234]        # CALL
        - * (FOR &SECURITY)                                   [0234]        # CALL
        ```
        动词模式分3部分，分别是动词解释，同义词块，句型模式。
        动词解释不需翻译；
        翻译同义词时，一个词可能有多个词义，取同语境相符的词义，比如CALL取“致电”和“呼叫”；
        翻译模式句型时，该动词可能产生新含义，如在CALL FOR PROTECTION 有"要求，呼吁"的含义，此时需要将"要求，呼吁"加到该同义词列表中。
    5.3 分工：
        王昌宝：line 702:1009
        盛文博：line 1013:1313
        张家培：line 1317:1608
        赵田阳：line 1612:1912
        丁瑞雪：line 1917:2214
        罗雅文：line: 1918:2476
        时鸿剑：line: 2480:2784