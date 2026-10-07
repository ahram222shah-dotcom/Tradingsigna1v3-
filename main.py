from kivy.app import App
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.properties import StringProperty, NumericProperty
from kivy.uix.boxlayout import BoxLayout
import random
from datetime import datetime

KV = """
<Root>:
    orientation: "vertical"
    padding: 14
    spacing: 8
    Label:
        text: "TRADING SIGNAL V3"
        font_size: 24
        bold: True
    Label:
        text: "ہر 10 سیکنڈ بعد تجزیاتی سگنل"
    Spinner:
        text: "BTC-USD"
        values: ["BTC-USD","ETH-USD","EURUSD","GBPUSD"]
        size_hint_y: None
        height: 48
    Label:
        text: "Price: " + root.price
        font_size: 18
    Label:
        text: "RSI: " + root.rsi + "    EMA9: " + root.ema9
    Label:
        text: "EMA21: " + root.ema21
    Label:
        text: root.signal
        font_size: 30
        bold: True
    Label:
        text: root.reason
    Label:
        text: "اگلا ریفریش: " + root.count
    Button:
        text: "ابھی سگنل چیک کریں"
        size_hint_y: None
        height: 52
        on_release: root.refresh()
    Label:
        text: root.status
"""

class Root(BoxLayout):
    price=StringProperty("--"); rsi=StringProperty("--")
    ema9=StringProperty("--"); ema21=StringProperty("--")
    signal=StringProperty("WAIT"); reason=StringProperty("انتظار کریں")
    count=StringProperty("10"); status=StringProperty("Ready")
    n=NumericProperty(10)
    prices=[]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_interval(self.timer,1)
        Clock.schedule_once(lambda dt:self.refresh(),.5)

    def timer(self,dt):
        self.n-=1
        if self.n<=0:
            self.n=10; self.refresh()
        self.count=str(int(self.n))

    def refresh(self):
        p=(self.prices[-1] if self.prices else 85200)+random.uniform(-45,45)
        self.prices.append(p); self.prices=self.prices[-60:]
        a=self.prices[:]
        while len(a)<22:a.insert(0,p)
        R=self.calc_rsi(a); E9=self.ema(a,9); E21=self.ema(a,21)
        if R<35 and E9>E21:sig,why="CALL / YES","RSI کم + EMA9 اوپر"
        elif R>65 and E9<E21:sig,why="PUT / NO","RSI زیادہ + EMA9 نیچے"
        else:sig,why="WAIT","واضح setup نہیں"
        self.price=f"{p:.2f}";self.rsi=f"{R:.2f}";self.ema9=f"{E9:.2f}";self.ema21=f"{E21:.2f}"
        self.signal=sig;self.reason=why
        self.status="Last update: "+datetime.now().strftime("%H:%M:%S")
        try:
            from jnius import autoclass
            PythonActivity=autoclass("org.kivy.android.PythonActivity")
            TTS=autoclass("android.speech.tts.TextToSpeech")
            Locale=autoclass("java.util.Locale")
            def ready(status):
                if status==TTS.SUCCESS:
                    tts.setLanguage(Locale("en","US"))
                    tts.speak(sig.replace("/"," "),TTS.QUEUE_FLUSH,None,"signal")
            tts=TTS(PythonActivity.mActivity,ready)
        except Exception: pass

    @staticmethod
    def ema(a,p):
        k=2/(p+1);e=a[0]
        for x in a[1:]:e=x*k+e*(1-k)
        return e
    @staticmethod
    def calc_rsi(a,p=14):
        g=l=0
        for i in range(len(a)-p,len(a)):
            d=a[i]-a[i-1]
            if d>0:g+=d
            else:l-=d
        if l==0:return 100
        rs=(g/p)/(l/p)
        return 100-100/(1+rs)

class AppV3(App):
    def build(self):
        Builder.load_string(KV)
        return Root()

AppV3().run()
