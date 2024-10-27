from functools import wraps
from dataclasses import dataclass
from typing import Type, Callable, List, Dict, Optional, get_origin
from types import UnionType
import re
from enum import Enum


class RequestType(Enum):
    QUERY = "q"
    BODY = "b"
    PATH = "p"
    QUERY_AND_PATH = "q|p"
    ALL = "q|b|p"
    UNKNOWN = ""


@dataclass
class TypeCheck:
    input_type: Type
    coerce: Type
    regex: Optional[str] = None
    coerce_function: Optional[Callable] = None
    pre_validate: Optional[Callable] = None


def is_equal_type(variable_type: Type, define_type: Type | UnionType) -> Type | None:
    target_types: List[Type] = []
    if get_origin(define_type) is UnionType:
        for v in define_type.__args__:
            target_types.append(v)
    else:
        target_types = [define_type]

    for target_type in target_types:
        if variable_type == target_type:
            return target_type
    return None


def input_coerce(defines: Dict[RequestType, TypeCheck]):

    def _input_coerce(func):

        @wraps(func)
        def _wrapper(*args, **kwargs):

            # バリデータの引数を参照する
            errors: dict = {}
            input_parameter: dict = {}
            key: str = ""
            coerced = None
            if len(args) > 0:
                errors = args[0]
            else:
                errors = kwargs.get("error", {})
            if len(args) > 1:
                input_parameter = args[1]
            else:
                input_parameter = kwargs.get("input", {})
            if len(args) > 2:
                key = args[2]
            else:
                key = kwargs.get("key", "")

            # 必須チェックを実施する
            required: bool = kwargs.get("required", False)
            # リクエストタイプを取得する
            request_type: RequestType = kwargs.get("request_type", None)

            # デコレートした関数の引数から、検証対象の変数を参照する
            variable = input_parameter.get(key)

            # 検証対象の変数がNoneであれば処理しない
            if variable is None:
                # 必須チェックが有効ならエラーを追加する
                if required is True:
                    errors[key] = f"Required: {key}"
                return False

            # 対象のリスト
            define_list: List[TypeCheck] = defines.values()

            if request_type is not None:
                # リクエストタイプに対応する入力定義を取得する
                # もし引数にリクエストタイプがあるなら、引数のリクエストタイプだけを検証する
                define: TypeCheck = None
                for d in defines.keys():
                    if request_type.value in d.value:
                        define_list = [defines[d]]
                        break

            for define in define_list:
                # 型を検証、引数の配列と一致する型なら処理をする
                target_type = is_equal_type(type(variable), define.input_type)
                if target_type is not None:

                    # 入力型を検証する
                    if target_type == str:
                        if define.regex is not None:
                            # 正規表現で検証、一致しないのならエラーを返す
                            if not re.match(define.regex, variable):
                                errors[key] = f'Regex Check Error: {key} : "{variable}"'
                                return False

                    # coerceが指定されていて、変換後の型と引数の型が異なるなら、キャストする
                    if define.coerce is not target_type:
                        # キャスト関数が例外を投げたのなら、エラーを返す
                        try:
                            if define.coerce_function is not None:
                                # キャスト関数が指定されているのなら、それを利用する
                                coerced = define.coerce_function(variable)
                            else:
                                # キャスト関数が指定されていないのなら、型変換を行う
                                coerced = define.coerce(variable)
                        except ValueError:
                            # キャストに失敗したのなら、エラーを返す
                            errors[key] = f"Cast Error: {key}"
                            return False
                    else:
                        # 変換後の型と引数の型が同じなら、そのままcoerce後の値として扱う
                        coerced = variable

                    # 事前判定があれば実行する
                    # 事前判定の例:
                    #     isfinite -> floatが有限かどうかを判定する
                    #     not_is_empty -> 空文字、空配列かどうかを判定する
                    if define.pre_validate is not None:
                        # 事前判定がFalseを返したのなら、それを実行する
                        if not define.pre_validate(coerced):
                            errors[key] = f"Pre-Validate Error: {key}"
                            return False

                    # 装飾した関数の引数に、coerce後の値を設定する
                    kwargs["coerced"] = coerced

                    # 装飾した関数を実行する
                    return func(*args, **kwargs)

            # 検証対象の型と一致しない場合、エラーを返す
            errors[key] = f"Undefined Type: {key}"
            return False

        return _wrapper

    return _input_coerce
