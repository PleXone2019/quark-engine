
import pytest
from androguard.core.mutf8 import MUTF8String
from androguard.core.analysis.analysis import MethodAnalysis

from quark.main import XRule
from quark.Objects.BytecodeObject import BytecodeObject


@pytest.fixture()
def xrule_obj1(scope="fuction"):
    apk_file = "quark/sample/13667fe3b0ad496a0cd157f34b7e0c991d72a4db.apk"
    xrule_obj = XRule(apk_file)
    yield xrule_obj


@pytest.fixture()
def xrule_obj2(scope="fuction"):
    apk_file = "quark/sample/14d9f1a92dd984d6040cc41ed06e273e.apk"
    xrule_obj = XRule(apk_file)
    yield xrule_obj


class TestXRule():

    def test_permissions(self, xrule_obj1):
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
        assert set(xrule_obj1.permissions) == set(ans)

    def test_find_method(self, xrule_obj1):
        result = list(xrule_obj1.find_method("Ljava/lang/reflect/Field"))
        assert len(result) == 2
        assert isinstance(result[0], MethodAnalysis)

    def test_upperFunc(self, xrule_obj1):
        result = xrule_obj1.upperFunc("Landroid/content/ContentResolver",
                                      "query")

        expect_cls = "Lcom/example/google/service/ContactsHelper;"
        expect_func = "getSIMContacts"
        expect_tuple = (
            MUTF8String.from_str(expect_cls),
            MUTF8String.from_str(expect_func),
        )
        # (Lcom/example/google/service/ContactsHelper;, getSIMContacts)

        assert expect_tuple in result

    def test_get_method_bytecode(self, xrule_obj1, xrule_obj2):
        target1_cls = "Lcom/example/google/service/ContactsHelper"
        target1_func = "query"
        result1 = xrule_obj1.get_method_bytecode(target1_cls, target1_func)
        assert len(list(result1)) == 0

        target2_cls = "Lcom/google/progress/AndroidClientService"
        target2_func = "sendMessage"
        result2 = xrule_obj2.get_method_bytecode(target2_cls, target2_func)
        result2_list = list(result2)
        assert len(result2_list) == 87
        result2_mne_para = [(i.mnemonic, i.parameter) for i in result2_list]
        expect_item = ("new-instance", "Lcom/google/progress/SMSHelper;")
        assert expect_item in result2_mne_para
