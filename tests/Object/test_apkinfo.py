import pytest
from androguard.core.analysis.analysis import MethodAnalysis

from quark.Objects.Apkinfo import Apkinfo


@pytest.fixture()
def apkinfo(scope="fuction"):
    apk_file = "quark/sample/13667fe3b0ad496a0cd157f34b7e0c991d72a4db.apk"
    apkinfo = Apkinfo(apk_file)
    yield apkinfo


class TestApkinfo():

    def test_permissions(self, apkinfo):
        ans = [
            'android.permission.SEND_SMS',
            'android.permission.RECEIVE_BOOT_COMPLETED',
            'android.permission.WRITE_SMS',
            'android.permission.READ_SMS',
            'android.permission.INTERNET',
            'android.permission.READ_PHONE_STATE',
            'android.permission.RECEIVE_SMS',
            'android.permission.READ_CONTACTS'
        ]
        assert set(apkinfo.permissions) == set(ans)

    def test_find_method(self, apkinfo):
        result = list(apkinfo.find_method("Ljava/lang/reflect/Field"))
        assert len(result) == 2
        assert isinstance(result[0], MethodAnalysis)

    def test_upperfunc(self, apkinfo):
        result = apkinfo.upperfunc("Ljava/lang/reflect/Field",
                                   "setAccessible")
        expect_func = "Landroid/support/v4/widget/SlidingPaneLayout$" \
                      "SlidingPanelLayoutImplJB;"
        assert expect_func in result[0]
