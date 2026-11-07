"""Headless Edge helpers for checking miminet front fixes against a local server."""

import time

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

BASE = "http://127.0.0.1:5000"


def make_driver(preload_js=None):
    opts = webdriver.EdgeOptions()
    opts.add_argument("--headless=new")
    opts.add_argument("--window-size=1600,1000")
    opts.set_capability("ms:loggingPrefs", {"browser": "ALL"})
    d = webdriver.Edge(options=opts)
    if preload_js:
        # Runs in the page's main world before any page script, like a
        # third-party/extension script that declares globals.
        d.execute_cdp_cmd(
            "Page.addScriptToEvaluateOnNewDocument", {"source": preload_js}
        )
    return d


def login(d, email="selenium", password="password"):
    d.get(BASE + "/auth/login.html")
    status = d.execute_async_script(
        """
        const done = arguments[arguments.length - 1];
        fetch('/auth/login.html', {method: 'POST', credentials: 'include',
            body: new URLSearchParams({email: arguments[0], password: arguments[1]})})
          .then(r => done(r.status + ' ' + r.url)).catch(e => done('ERR ' + e));
        """,
        email,
        password,
    )
    return status


def new_network(d):
    d.get(BASE + "/create_network")
    WebDriverWait(d, 20).until(EC.presence_of_element_located((By.ID, "network_scheme")))
    WebDriverWait(d, 20).until(lambda drv: drv.execute_script("return typeof global_cy !== 'undefined' && !!global_cy"))
    return d.current_url.split("guid=")[-1]


def drop_device(d, device_id, dx=0, dy=0):
    """Drag a device from the left panel onto the scheme (real jQuery UI drag)."""
    src = d.find_element(By.ID, device_id)
    dst = d.find_element(By.ID, "network_scheme")
    ActionChains(d).click_and_hold(src).move_by_offset(5, 5).move_to_element_with_offset(
        dst, dx, dy
    ).release().perform()
    time.sleep(0.5)


def connect(d, source_id, target_id):
    """Same calls as the edgehandles `ehcomplete` handler in netfront_f.js."""
    return d.execute_script(
        """
        try {
            AddEdge(arguments[0], arguments[1]);
            DrawGraph(); PostNodesEdges();
            return 'ok';
        } catch (e) { return e.constructor.name + ': ' + e.message; }
        """,
        source_id,
        target_id,
    )


def node_ids(d):
    return d.execute_script("return nodes.map(n => n.data.id)")


def edges_info(d):
    return d.execute_script("return edges.map(e => e.data.source + '->' + e.data.target)")


def severe_console(d):
    return [e["message"] for e in d.get_log("browser") if e["level"] == "SEVERE"]
