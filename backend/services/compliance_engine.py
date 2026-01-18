"""
Compliance Engine - Core Compliance Checking Logic
Detects violations in real-time and provides guidance
"""

from typing import List, Dict, Optional
from loguru import logger
from datetime import datetime
import re
import asyncio


class ComplianceRule:
    """Represents a single compliance rule"""
    
    def __init__(
        self,
        rule_id: str,
        name: str,
        category: str,
        patterns: List[str],
        severity: str,
        message: str,
        suggested_response: Optional[str] = None,
        regulation_reference: Optional[str] = None,
    ):
        self.rule_id = rule_id
        self.name = name
        self.category = category
        self.patterns = [re.compile(p, re.IGNORECASE) for p in patterns]
        self.severity = severity
        self.message = message
        self.suggested_response = suggested_response
        self.regulation_reference = regulation_reference
    
    def check(self, text: str) -> bool:
        """Check if text matches this rule"""
        return any(pattern.search(text) for pattern in self.patterns)


class ComplianceEngine:
    """
    Main compliance engine that checks for violations
    """
    
    def __init__(self):
        self.rules: List[ComplianceRule] = []
        self.initialized = False
    
    async def initialize(self):
        """Initialize compliance rules"""
        logger.info("Initializing Compliance Engine...")
        
        # Load default rules
        self._load_default_rules()
        
        # TODO: Load custom rules from database
        # TODO: Load FDA regulations using Token Company
        
        self.initialized = True
        logger.success(f"Compliance Engine initialized with {len(self.rules)} rules")
    
    def _load_default_rules(self):
        """Load default compliance rules"""
        
        # Off-Label Promotion Rules
        self.rules.append(ComplianceRule(
            rule_id="off_label_001",
            name="Direct Off-Label Promotion",
            category="off_label",
            patterns=[
                r"this (drug|medication|product) (can|will) (help|treat|cure) (?!.*approved)",
                r"you can use (this|it) for (weight loss|PCOS|prediabetes)",
                r"it('s| is) (great|perfect|effective) for (?!.*FDA.*approved)",
                r"many doctors use (this|it) for",
            ],
            severity="critical",
            message="🛑 Off-label promotion detected. You cannot promote unapproved uses.",
            suggested_response="I can only discuss the FDA-approved indication. Would you like to hear about the clinical data for [approved use]?",
            regulation_reference="FDA FDCA Section 502(f)(1)",
        ))
        
        self.rules.append(ComplianceRule(
            rule_id="off_label_002",
            name="Implied Off-Label Use",
            category="off_label",
            patterns=[
                r"patients have seen (results|benefits|improvements) in",
                r"some doctors prescribe (this|it) for",
                r"it('s| is) commonly used for",
            ],
            severity="warning",
            message="⚠️ Be careful - this sounds like implied off-label use.",
            suggested_response="I can only speak to our FDA-approved indication for [indication].",
            regulation_reference="FDA Guidance on Off-Label Promotion",
        ))
        
        # Efficacy Exaggeration Rules
        self.rules.append(ComplianceRule(
            rule_id="efficacy_001",
            name="Absolute Efficacy Claims",
            category="efficacy",
            patterns=[
                r"(100%|completely|totally|always) (effective|works)",
                r"(cures|eliminates|removes) (all|every)",
                r"guaranteed (results|to work)",
                r"never fails",
            ],
            severity="critical",
            message="🛑 Absolute efficacy claim detected. Use data-backed language.",
            suggested_response="In clinical trials, [X%] of patients experienced [specific outcome].",
            regulation_reference="FDA Guidance on Drug Advertising",
        ))
        
        self.rules.append(ComplianceRule(
            rule_id="efficacy_002",
            name="Comparative Superiority without Data",
            category="efficacy",
            patterns=[
                r"(better|superior|more effective) than (?!.*study|.*trial)",
                r"(best|#1|number one) (drug|medication|treatment)",
                r"beats (all|every) (competitor|other)",
            ],
            severity="warning",
            message="⚠️ Comparative claim requires clinical data support.",
            suggested_response="Would you like to see the head-to-head trial data?",
            regulation_reference="FDA Guidance on Comparative Claims",
        ))
        
        # Safety/Side Effect Rules
        self.rules.append(ComplianceRule(
            rule_id="safety_001",
            name="Downplaying Side Effects",
            category="safety",
            patterns=[
                r"(side effects|risks) (are|is) (minimal|minor|nothing to worry about)",
                r"(rarely|almost never) (causes|has) side effects",
                r"(don't|do not) worry about (side effects|risks)",
            ],
            severity="critical",
            message="🛑 Cannot minimize side effects. Provide balanced information.",
            suggested_response="The most common side effects include [list]. Please see the full prescribing information.",
            regulation_reference="FDA FDCA Section 502(n)",
        ))
        
        # Contraindication Rules
        self.rules.append(ComplianceRule(
            rule_id="contraindication_001",
            name="Ignoring Contraindications",
            category="contraindications",
            patterns=[
                r"(pregnant|pregnancy) (is|are) (fine|okay|not a problem)",
                r"(don't|do not) worry about (kidney|liver|heart) (problems|issues)",
                r"contraindication(s?) (don't|do not) (really matter|apply)",
            ],
            severity="critical",
            message="🛑 Cannot dismiss contraindications. This is a patient safety issue.",
            suggested_response="This medication has contraindications for [conditions]. Please review the prescribing information carefully.",
            regulation_reference="FDA Prescribing Information Requirements",
        ))
        
        # Pricing/Payment Rules
        self.rules.append(ComplianceRule(
            rule_id="pricing_001",
            name="Illegal Pricing Discussions",
            category="pricing",
            patterns=[
                r"(kickback|rebate|discount) for (prescribing|using)",
                r"I('ll| will) give you",
                r"special (deal|offer|pricing) if you",
            ],
            severity="critical",
            message="🛑 This sounds like an illegal inducement. Stop immediately.",
            suggested_response="Our pricing follows all federal guidelines. I can connect you with our reimbursement team.",
            regulation_reference="Anti-Kickback Statute (42 U.S.C. § 1320a-7b)",
        ))
        
        # Confidence/Uncertainty Patterns
        self.rules.append(ComplianceRule(
            rule_id="confidence_001",
            name="Uncertain Response",
            category="confidence",
            patterns=[
                r"(I think|maybe|possibly|I'm not sure|I don't know)",
                r"(um+|uh+|er+){2,}",  # Multiple filler words
            ],
            severity="info",
            message="💡 You sound uncertain. Pivot to clinical data or defer to materials.",
            suggested_response="Let me reference the clinical data to give you an accurate answer.",
            regulation_reference=None,
        ))
    
    async def check_text(
        self,
        text: str,
        context: Optional[Dict] = None,
    ) -> List[Dict]:
        """
        Check text for compliance violations
        Returns list of violations found
        """
        violations = []
        
        if not self.initialized:
            logger.warning("Compliance engine not initialized")
            return violations
        
        # Check against all rules
        for rule in self.rules:
            if rule.check(text):
                violation = {
                    "rule_id": rule.rule_id,
                    "rule_name": rule.name,
                    "category": rule.category,
                    "severity": rule.severity,
                    "message": rule.message,
                    "suggested_response": rule.suggested_response,
                    "regulation_reference": rule.regulation_reference,
                    "matched_text": text,
                    "timestamp": datetime.utcnow().isoformat(),
                }
                violations.append(violation)
                
                logger.warning(
                    f"Violation detected: {rule.name} ({rule.severity})"
                )
        
        return violations
    
    async def check_transcript_segment(
        self,
        speaker: str,
        text: str,
        session_context: Optional[Dict] = None,
    ) -> List[Dict]:
        """
        Check a transcript segment for violations
        Only checks rep's speech, not doctor's
        """
        if speaker != "rep":
            return []
        
        return await self.check_text(text, context=session_context)
    
    def add_custom_rule(self, rule: ComplianceRule):
        """Add a custom compliance rule"""
        self.rules.append(rule)
        logger.info(f"Added custom rule: {rule.rule_id}")
    
    def get_rules_by_category(self, category: str) -> List[ComplianceRule]:
        """Get all rules for a specific category"""
        return [rule for rule in self.rules if rule.category == category]
    
    async def generate_coaching_tip(
        self,
        text: str,
        violations: List[Dict],
    ) -> Optional[str]:
        """
        Generate a coaching tip based on the violations detected
        """
        if not violations:
            return None
        
        # Priority: critical > warning > info
        severity_priority = {"critical": 0, "warning": 1, "info": 2}
        violations.sort(key=lambda v: severity_priority.get(v["severity"], 999))
        
        top_violation = violations[0]
        
        # Return suggested response if available
        if top_violation.get("suggested_response"):
            return top_violation["suggested_response"]
        
        return f"Avoid discussing {top_violation['category']}. Stick to approved messaging."
