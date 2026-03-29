import difflib
from typing import Dict, List

TASKS = [
    {
        "id": "syntax_error",
        "description": (
            "Review the following JavaScript code. "
            "It has syntax errors. Identify all issues in the 'issues' field "
            "and provide corrected code in 'fixed_code'."
        ),
        "language": "javascript",
        "code": """\
function calculateTotal(items) {
    let total = 0
    for (let i = 0; i < items.length; i++ {
        total += items[i].price
    }
    return total
""",
        "expected_issues_keywords": [
            "semicolon", "parenthes", "closing", "syntax", "brace", "bracket", "missing"
        ],
        "expected_fixed": """\
function calculateTotal(items) {
    let total = 0;
    for (let i = 0; i < items.length; i++) {
        total += items[i].price;
    }
    return total;
}
""",
    },

    {
        "id": "logic_bug",
        "description": (
            "Review the following Python code. "
            "The function is supposed to return the second largest unique number in a list "
            "but it has a logic bug. Identify the issue in 'issues' and provide a fix in 'fixed_code'."
        ),
        "language": "python",
        "code": """\
def second_largest(nums):
    unique = list(set(nums))
    unique.sort()
    return unique[-1]
""",
        "expected_issues_keywords": [
            "second", "largest", "-2", "index", "last", "wrong", "returns", "instead", "off"
        ],
        "expected_fixed": """\
def second_largest(nums):
    unique = list(set(nums))
    unique.sort()
    return unique[-2]
""",
    },

    {
        "id": "full_review",
        "description": (
            "Perform a full code review of the following Java code. "
            "Identify ALL issues: logic bugs, naming convention violations, "
            "inefficiencies, and poor practices. "
            "Provide a fully corrected version in 'fixed_code'."
        ),
        "language": "java",
        "code": """\
public class helper {
    public static int[] removeDuplicates(int[] arr) {
        int[] temp = new int[arr.length];
        int count = 0;
        for (int i = 0; i < arr.length; i++) {
            boolean found = false;
            for (int j = 0; j < count; j++) {
                if (temp[j] == arr[i]) {
                    found = true;
                    break;
                }
            }
            if (!found) {
                temp[count] = arr[i];
                count++;
            }
        }
        return temp;
    }
}
""",
        "expected_issues_keywords": [
            "naming", "class", "pascal", "uppercase", "helper",
            "inefficien", "o(n", "quadratic", "set", "hashset",
            "return", "length", "extra", "unused", "array"
        ],
        "expected_fixed": """\
import java.util.LinkedHashSet;
import java.util.Set;

public class Helper {
    public static int[] removeDuplicates(int[] arr) {
        Set<Integer> seen = new LinkedHashSet<>();
        for (int num : arr) {
            seen.add(num);
        }
        return seen.stream().mapToInt(Integer::intValue).toArray();
    }
}
""",
    },
]

TASK_MAP = {t["id"]: t for t in TASKS}


def _keyword_score(issues: List[str], expected_keywords: List[str]) -> float:
    issues_text = " ".join(issues).lower()
    hits = sum(1 for kw in expected_keywords if kw.lower() in issues_text)
    return min(hits / max(len(expected_keywords), 1), 1.0)


def _similarity_score(fixed_code: str, expected_fixed: str) -> float:
    if not fixed_code.strip():
        return 0.0
    return difflib.SequenceMatcher(None, fixed_code.strip(), expected_fixed.strip()).ratio()


def grade(task_id: str, issues: List[str], fixed_code: str) -> float:
    task = TASK_MAP.get(task_id)
    if not task:
        return 0.0

    keyword_score = _keyword_score(issues, task["expected_issues_keywords"])
    similarity_score = _similarity_score(fixed_code, task["expected_fixed"])

    final = round((0.5 * keyword_score) + (0.5 * similarity_score), 4)
    return min(final, 1.0)
