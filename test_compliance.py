"""
Quick Test Script for Veritas Compliance Engine
Run this to test the compliance rules without starting the full app
"""

import asyncio
from backend.services.compliance_engine import ComplianceEngine


async def test_compliance_engine():
    """Test the compliance engine with various scenarios"""
    
    print("🧪 Testing Veritas Compliance Engine")
    print("=" * 50)
    print()
    
    # Initialize engine
    engine = ComplianceEngine()
    await engine.initialize()
    
    print(f"✅ Loaded {len(engine.rules)} compliance rules")
    print()
    
    # Test scenarios
    test_cases = [
        {
            "name": "Off-Label Promotion",
            "text": "This drug can help with weight loss in your patients.",
            "expected": "critical",
        },
        {
            "name": "Absolute Efficacy Claim",
            "text": "This medication is 100% effective and always works.",
            "expected": "critical",
        },
        {
            "name": "Downplaying Side Effects",
            "text": "Don't worry about side effects, they're minimal.",
            "expected": "critical",
        },
        {
            "name": "Uncertain Response",
            "text": "Um, I think maybe it works, but I'm not sure...",
            "expected": "info",
        },
        {
            "name": "Compliant Statement",
            "text": "In clinical trials, 78% of patients achieved a 1.5% reduction in A1C.",
            "expected": None,
        },
    ]
    
    for i, test in enumerate(test_cases, 1):
        print(f"Test {i}: {test['name']}")
        print(f"Rep says: \"{test['text']}\"")
        
        violations = await engine.check_text(test['text'])
        
        if violations:
            print(f"⚠️  Violations detected: {len(violations)}")
            for violation in violations:
                print(f"   - {violation['severity'].upper()}: {violation['message']}")
                if violation.get('suggested_response'):
                    print(f"   💡 Suggest: \"{violation['suggested_response']}\"")
        else:
            print("✅ No violations detected")
        
        print()
    
    print("=" * 50)
    print("✅ All tests completed!")


if __name__ == "__main__":
    asyncio.run(test_compliance_engine())
